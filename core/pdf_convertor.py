import subprocess
import os
from constants.variables import *
from constants.msg import ErrorType
from core.error_block import ErrorBlocker


class Convert2PDF:

    def __init__(self,
                 file_path: str,
                 newfilename: str,
                 username: str):
        # Todo под расширение для других форматов
        self.file = file_path
        self.new = newfilename
        self.username = username

    def DocxToPdf(self):
        directory = self.username
        with open("error.txt", "w") as file:
            file.write(f"{os.getcwd()}\n")
            file.write(f"{os.path.isdir(directory)}\n")
            file.write(f"{FILE_FOLDER + directory}\n")
            file.write(f"{self.file}\n")
        if os.path.isdir(directory) == False:
            return ErrorBlocker().process(ErrorType.missing_doc)
        subprocess.call(['/usr/bin/soffice',
                         '--headless',
                         '--convert-to',
                         'pdf',
                         '--outdir',
                         directory,
                         self.file[3:]])
        old = self.file.replace('.docx', '.pdf')[3:]
        new = directory + '/' + self.new + '.pdf'
        subprocess.call(['mv', old, new])
        if os.path.exists(new):
            return new
        return ErrorBlocker().process(ErrorType.missing_doc)
