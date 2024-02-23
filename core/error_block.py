from constants.msg import *


class ErrorBlocker:

    def process(self, error_type: int):
        return ERROR_MSG[error_type]