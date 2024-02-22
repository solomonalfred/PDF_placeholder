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
        directory = FILE_FOLDER + "volumes/" + self.username
        if os.path.isdir(directory) == False:
            return ErrorBlocker().process(ErrorType.missing_doc)
        print(directory)
        subprocess.call(['/usr/bin/soffice',
                         '--headless',
                         '--convert-to',
                         'pdf',
                         '--outdir',
                         directory,
                         self.file])
        old = self.file.replace('.docx', '.pdf')
        new = directory + '/' + self.new + '.pdf'
        subprocess.call(['mv', old, new])
        if os.path.exists(new):
            return new
        return ErrorBlocker().process(ErrorType.missing_doc)
