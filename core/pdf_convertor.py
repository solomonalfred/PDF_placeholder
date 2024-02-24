import subprocess
import os
from constants.variables import *
from constants.msg import ErrorType
from constants.core_items import *
from core.error_block import ErrorBlocker


class Convert2PDF:

    def __init__(self,
                 file_path: str,
                 newfilename: str,
                 username: str):
        self.file = file_path
        self.new = newfilename
        self.username = username

    def DocxToPdf(self):
        directory = os.path.join(FILE_FOLDER, self.username)
        if os.path.isdir(directory) == False:
            return ErrorBlocker().process(ErrorType.missing_doc)
        convert = PDF_CONVERT
        convert[5] = directory
        convert[6] = self.file
        subprocess.call(convert)
        # os.remove(self.file)
        old = self.file.replace(Process_items.NEW_DOCX, PDF_items.PDF_TMP)
        new = os.path.join(directory, self.new + PDF_items.PDF)
        subprocess.call([PDF_items.MOVE, old, new])
        if os.path.exists(new):
            return new
        return ErrorBlocker().process(ErrorType.missing_doc)
