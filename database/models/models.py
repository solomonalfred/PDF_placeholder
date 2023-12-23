from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, TIMESTAMP, DECIMAL, Boolean
from datetime import datetime

metadata = MetaData()


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("nickname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("balance", DECIMAL, default=5000),
    Column("role", String, nullable=False),
    Column("unlimited", Boolean, default=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow)
)

pdf_file = Table(
    "pdf_file",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("sizeBytes", Integer, nullable=False),
    Column("path", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("user_id", Integer, ForeignKey("user.id"))
)

docx_file = Table(
    "docx_file",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("path", String, nullable=False),
    Column("sizeBytes", Integer, nullable=False),
    Column("deleted", Boolean, default=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("user_id", Integer, ForeignKey("user.id"))
)

transaction = Table(
    "transaction",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False),
    Column("amount", DECIMAL, nullable=False),
    Column("balance", DECIMAL, nullable=False),
    Column("page_processed", Integer, default=0),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("file", String, default=""),
    Column("template", Integer, ForeignKey("docx_file.id")),
    Column("unlimited", Boolean, default=False),
    Column("user_id", Integer, ForeignKey("user.id"))
)
