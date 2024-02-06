from sqlalchemy import insert, select, update, delete
from database.models.models import *
from database.SQL_session import *
import asyncio
from decimal import Decimal


async def add_user(name: str,
                   nickname: str,
                   email: str,
                   telegram_id: str,
                   password: str,
                   role: str,
                   session: AsyncSession) -> int:
    stmt = insert(user).values(
        name=name,
        nickname=nickname,
        email=email,
        telegramID=telegram_id,
        password=password,
        role=role,
        unlimited=False
    ).returning(user.c.id)

    result = await session.execute(stmt)
    user_id = result.scalar_one()
    await session.commit()

    return user_id


async def add_user_if_not_exists(session: AsyncSession,
                                 name: str,
                                 nickname: str,
                                 email: str,
                                 telegram_id: str,
                                 password: str,
                                 role: str,
                                 balance: int = 5000,
                                 unlimited: bool = True):
    stmt = select(user).where(user.c.nickname == nickname,
                              user.c.email == email,
                              user.c.telegramID == telegram_id)
    result = await session.execute(stmt)
    user_exists = result.scalar_one_or_none() is not None

    if not user_exists:
        stmt = insert(user).values(
            name=name,
            nickname=nickname,
            email=email,
            telegramID=telegram_id,
            password=password,
            balance=balance,
            role=role,
            unlimited=unlimited,
            registered_at=datetime.utcnow()
        )
        await session.execute(stmt)
        await session.commit()


async def update_user(session: AsyncSession,
                                 name: str,
                                 nickname: str,
                                 email: str,
                                 telegram_id: str,
                                 password: str,
                                 role: str,
                                 balance: int,
                                 unlimited: bool = True):
    try:
        update_user_stmt = (update(user)
        .where(user.c.nickname == nickname)
        .values(
            name=name,
            email=email,
            telegramID=telegram_id,
            password=password,
            balance=balance,
            role=role,
            unlimited=unlimited
        ))
        await session.execute(update_user_stmt)
        await session.commit()
        return True
    except:
        return False



async def find_user_by_nickname(session: AsyncSession, nickname: str):
    stmt = select(user).where(user.c.nickname == nickname)
    result = await session.execute(stmt)
    user_record = result.one_or_none()

    if user_record:
        # Преобразование данных пользователя в словарь
        return {
            "id": user_record.id,
            "name": user_record.name,
            "nickname": user_record.nickname,
            "email": user_record.email,
            "telegramID": user_record.telegramID,
            "balance": int(user_record.balance),
            "password": user_record.password,
            "role": user_record.role,
            "unlimited": user_record.unlimited,
            "registered_at": user_record.registered_at
        }
    else:
        return None


async def find_user_by_email(session: AsyncSession, email: str):
    stmt = select(user).where(user.c.email == email)
    result = await session.execute(stmt)
    user_record = result.one_or_none()

    if user_record:
        return {
            "id": user_record.id,
            "name": user_record.name,
            "nickname": user_record.nickname,
            "email": user_record.email,
            "telegramID": user_record.telegramID,
            "balance": int(user_record.balance),
            "password": user_record.password,
            "role": user_record.role,
            "unlimited": user_record.unlimited,
            "registered_at": user_record.registered_at
        }
    else:
        return None

async def find_user_by_telegram(session: AsyncSession, tID: str):
    stmt = select(user).where(user.c.telegramID == tID)
    result = await session.execute(stmt)
    user_record = result.one_or_none()

    if user_record:
        return {
            "id": user_record.id,
            "name": user_record.name,
            "nickname": user_record.nickname,
            "email": user_record.email,
            "telegramID": user_record.telegramID,
            "balance": int(user_record.balance),
            "password": user_record.password,
            "role": user_record.role,
            "unlimited": user_record.unlimited,
            "registered_at": user_record.registered_at
        }
    else:
        return None

async def add_or_update_docx_file(session: AsyncSession, name: str, path: str, sizeBytes: int, user_id: int) -> int:
    # Поиск существующей записи
    stmt = select(docx_file).where(docx_file.c.name == name, docx_file.c.user_id == user_id)
    result = await session.execute(stmt)
    existing_file = result.one_or_none()

    if existing_file:
        stmt = (
            update(docx_file)
            .where(docx_file.c.id == existing_file.id)
            .values(path=path, sizeBytes=sizeBytes, deleted=False, created_at=datetime.utcnow())
            .returning(docx_file.c.id)
        )
    else:
        stmt = (
            insert(docx_file)
            .values(name=name, path=path, sizeBytes=sizeBytes, user_id=user_id, created_at=datetime.utcnow())
            .returning(docx_file.c.id)
        )

    result = await session.execute(stmt)
    file_id = result.scalar_one()
    await session.commit()

    return file_id

async def find_docx_file(session: AsyncSession, user_id: int, name: str) -> dict:
    stmt = select(docx_file).where(docx_file.c.user_id == user_id, docx_file.c.name == name)
    result = await session.execute(stmt)
    file_record = result.one_or_none()

    if file_record:
        # Преобразование данных файла в словарь
        return {
            "id": file_record.id,
            "name": file_record.name,
            "path": file_record.path,
            "sizeBytes": file_record.sizeBytes,
            "deleted": file_record.deleted,
            "created_at": file_record.created_at,
            "user_id": file_record.user_id
        }
    else:
        return None


async def find_docx_file_by_id(session: AsyncSession, user_id: int, name_id: str) -> str:
    stmt = select(docx_file).where(docx_file.c.user_id == user_id, docx_file.c.id == name_id)
    result = await session.execute(stmt)
    file_record = result.one_or_none()

    if file_record:
        return file_record.name
    else:
        return None

async def find_docx_files(session: AsyncSession, user_id: int) -> list:
    stmt = select(docx_file.c.name)\
        .where(docx_file.c.user_id == user_id,
               docx_file.c.deleted == False)
    result = await session.execute(stmt)
    file_records = result.scalars().all()

    return file_records

async def delete_docx_file(session: AsyncSession, user_id: int, name: str) -> bool:
    file_stmt = select(docx_file.c.id)\
        .where(docx_file.c.user_id == user_id, docx_file.c.name == name, docx_file.c.deleted == False)
    file_result = await session.execute(file_stmt)
    file_record = file_result.scalar_one_or_none()

    if file_record:
        update_stmt = update(docx_file).where(docx_file.c.id == file_record).values(deleted=True)
        await session.execute(update_stmt)

        await session.commit()
        return True

    return False

async def transaction_credit(session: AsyncSession,
                             user_id: int,
                             pdf_file: str,
                             docx_file_id: int,
                             credit_type: str,
                             amount: float,
                             page_processed: int) -> bool:
    # Находим последнюю транзакцию пользователя
    last_transaction_stmt = select(transaction).\
        where(transaction.c.user_id == user_id).\
        order_by(transaction.c.created_at.desc()).\
        limit(1)
    last_transaction_result = await session.execute(last_transaction_stmt)
    last_transaction = last_transaction_result.one_or_none()

    # Находим текущий баланс пользователя
    user_stmt = select(user.c.balance, user.c.unlimited).where(user.c.id == user_id)
    user_result = await session.execute(user_stmt)
    current_user_balance = user_result.one_or_none()

    if current_user_balance.unlimited:
        if last_transaction:
            new_balance = last_transaction.balance
        else:
            new_balance = current_user_balance.balance
    else:
        if last_transaction:
            new_balance = last_transaction.balance - Decimal(amount)
        else:
            new_balance = current_user_balance.balance - Decimal(amount)

        if new_balance < 0:
            return False

    # Создание новой записи в transactions
    new_transaction_stmt = insert(transaction).values(
        type=credit_type,
        amount=amount,
        balance=new_balance,
        page_processed=page_processed,
        created_at=datetime.utcnow(),
        file=pdf_file,
        template=docx_file_id,
        unlimited=current_user_balance.unlimited,
        user_id=user_id
    )
    await session.execute(new_transaction_stmt)

    # Обновление баланса пользователя в таблице user
    update_user_stmt = update(user).where(user.c.id == user_id).values(balance=new_balance)
    await session.execute(update_user_stmt)

    await session.commit()
    return True

async def transaction_debit(session: AsyncSession,
                            user_id: int,
                            amount: Decimal,
                            unlimited: bool = False) -> bool:

    # Находим последнюю транзакцию пользователя
    last_transaction_stmt = select(transaction).where(transaction.c.user_id == user_id).order_by(transaction.c.created_at.desc()).limit(1)
    last_transaction_result = await session.execute(last_transaction_stmt)
    last_transaction = last_transaction_result.one_or_none()

    # Находим текущий баланс пользователя
    user_stmt = select(user.c.balance, user.c.unlimited).where(user.c.id == user_id)
    user_result = await session.execute(user_stmt)
    current_user_balance = user_result.one_or_none()

    if last_transaction:
        new_balance = last_transaction.balance + amount
    else:
        new_balance = current_user_balance.balance + amount

    if unlimited or current_user_balance.unlimited:
        new_transaction_stmt = insert(transaction).values(
            type='debit',
            amount=amount,
            balance=new_balance,
            created_at=datetime.utcnow(),
            unlimited=True,
            user_id=user_id
        )
    else:
        new_transaction_stmt = insert(transaction).values(
            type='debit',
            amount=amount,
            balance=new_balance,
            created_at=datetime.utcnow(),
            unlimited=current_user_balance.unlimited,
            user_id=user_id
        )

    await session.execute(new_transaction_stmt)

    if unlimited:
        update_user_stmt = update(user).where(user.c.id == user_id).values(balance=new_balance, unlimited=True)
    else:
        update_user_stmt = update(user)\
            .where(user.c.id == user_id)\
            .values(balance=new_balance)
    await session.execute(update_user_stmt)

    await session.commit()
    return new_balance

async def add_or_update_pdf_file(session: AsyncSession,
                                 name: str,
                                 sizeBytes: int,
                                 path: str,
                                 user_id: int,
                                 page_processed: int,
                                 docx_file_name: str) -> bool:

    # Проверка наличия записи в pdf_files
    pdf_file_stmt = select(pdf_file).where(pdf_file.c.name == name, pdf_file.c.user_id == user_id)
    pdf_file_result = await session.execute(pdf_file_stmt)
    pdf_file_record = pdf_file_result.one_or_none()

    # Получение ID файла DOCX
    docx_file_stmt = select(docx_file.c.id).\
        where(docx_file.c.name == docx_file_name,
              docx_file.c.user_id == user_id,
              docx_file.c.deleted == False)
    docx_file_result = await session.execute(docx_file_stmt)
    docx_file_id = docx_file_result.scalar_one()

    # Выполнение транзакции
    transaction_success = await transaction_credit(session,
                                                   user_id,
                                                   name,
                                                   docx_file_id,
                                                    "credit",
                                                   page_processed,
                                                   page_processed)

    if transaction_success:
        if pdf_file_record:
            update_stmt = update(pdf_file).where(pdf_file.c.id == pdf_file_record.id).values(
                sizeBytes=sizeBytes,
                path=path,
                created_at=datetime.utcnow()
            )
            await session.execute(update_stmt)
        else:
            # Добавление новой записи
            insert_stmt = insert(pdf_file).values(
                name=name,
                sizeBytes=sizeBytes,
                path=path,
                created_at=datetime.utcnow(),
                user_id=user_id
            )
            await session.execute(insert_stmt)

        await session.commit()
        return True
    else:
        return False


async def transaction_list_(session: AsyncSession,
                            user_id: int):
    transaction_stmt = select(transaction). \
        where(transaction.c.user_id == user_id)
    transaction_result = await session.execute(transaction_stmt)
    result = transaction_result.fetchall()
    return [row._asdict() for row in result]

if __name__ == "__main__":
    async def main():
        async with get_async_session() as session:
            user_id = await add_user("Имя", "Никнейм", "email@example.com", "securepassword", session)
            print(f"Пользователь добавлен с ID: {user_id}")

    asyncio.run(main())
