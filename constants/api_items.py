class Table_items:
    ID = 'id'
    NAME = "name"
    NICKNAME = "nickname"
    EMAIL = "email"
    TELEGRAM_ID = "telegramID"
    PASSWORD = "password"
    BALANCE = "balance"
    ROLE = "role"
    UNLIMITED = "unlimited"
    REGISTERED_AT = "registered_at"

    SIZE_BYTES = "sizeBytes"
    PATH = "path"
    CRATED_AT = "created_at"
    USER_ID = "user_id"
    DELETED = "deleted"

    TYPE = 'type'
    AMOUNT = "amount"
    PAGE_PROCESSED = "page_processed"
    FILE = "file"
    TEMPLATE = "template"


class msg:
    MSG = 'msg'
    CREDENTIAL_EXEPTION = "Credentials exception"
    INTERNAL_SERVER_ERROR = "Internal server error"
    WRONG_DOCUMENT_FORMAT = "Wrong document format"
    INSUFFICIENT_FUNDS = "Insufficient funds"
    TEMPLATE_NOT_EXISTS = "Bad request. Template do not exist"
    NOT_FOUND = "Item not found"
    ACCESS_DENIED = "Access denied"
    TP_DELETED = "Template deleted"
    NO_TP = "There's no this template"
    SUCCESS_REFRESH = "Success refreshed password"

    DELETED = 'Deleted'

    TEMPLATES = "templates"
    BALANCE = "balance"


class server_path:
    KEYS = "{}/tags"
    RENDER = "{}/process"
    RENDER_LINK = "{}/process"
    TEMPLATES = "{}/list_templates"
    DELETE = "{}/delete_template"
    BALANCE = "{}/replenishment_balance"
    TRANSACTIONS = "{}/transaction_list"
    PASSWORD = "{}/refresh_password"

class Details:
    RESPONCE = "response"
    COUNT_TAGS = "count_tags"
    COUNT_TB = "count_tables"
    KEYS = "keys"
    TB = "tables"

    FILENAME = "filename"
    NEW_FILENAME = "newfilename"
    USERNAME = "username"
    TEMPLATENAME = 'templatename'
    TRANSACTIONS = "transactions"

    ROLE = 'role'
    ADMIN = 'admin'

    TELEGRAM_ID = "telegram_id"
    AMOUNT = "amount"
    UNLIMITED = "unlimited"
    COMMON = "Common"
    NEW_PASSWORD = "new_password"

    URL = 'url'

    RATE = "rate"

    DEBIT = 'debit'
    CREDIT = "credit"


LINK_URL = "{}/link/file?{}"


class Excel_items:
    ENGINE = 'xlsxwriter'
    SHEET = 'Лист1'
    HEADER = 'bold'

    MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    HEADER_RESPONCE_KEY = "Content-Disposition"
    HEADER_RESPONCE_VALUE = "attachment; filename=report.xlsx"



