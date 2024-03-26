
class EndpointsStatus:
    DB_NAME = "PDF_placeholder"
    COLLECT_NAME = "endpoints"
    KEYS = "keys"
    RENDER = "render"
    RENDER_LINK = "render_link"
    TEMPLATES = "templates"
    DELETE_TEMPLATE = "delete_template"
    TOPUP_USER = "topup_user"
    TRANSACTIONS = "transactions"
    TRANSACTIONS_EXPORT = "transactions_export"
    RESET_PASSWORD = "reset_password"

    ENDPOINTS = [KEYS,
                 RENDER,
                 RENDER_LINK,
                 TEMPLATES,
                 DELETE_TEMPLATE,
                 TOPUP_USER,
                 TRANSACTIONS,
                 TRANSACTIONS_EXPORT,
                 RESET_PASSWORD]

    WORKERS = ["W1", "W2", "W3", "W4"]

    SERVERS = {WORKERS[0]: "http://localhost:8001",
               WORKERS[1]: "http://localhost:8002",
               WORKERS[2]: "http://localhost:8003",
               WORKERS[3]: "http://localhost:8004"}

