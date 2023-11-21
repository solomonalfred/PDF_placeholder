MISSING_FILE = "Файл отстутствует"
NOT_FOUND_USER = "Пользователь не найден"

class ErrorType:
    ok = 0
    incorrect_doc = 1
    internal_error = 2
    missing_doc = 3

ERROR_MSG = {1: "Incorrect file",
             2: "Internal error",
             3: "Missing file"}