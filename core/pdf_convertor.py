import subprocess
import os
from constants.variables import *
from constants.msg import ErrorType


class Convert2PDF:

    def __init__(self,
                 file_path: str,
                 newfilename: str,
                 username: str):
        # Todo под расширение для других форматов
        self.file = file_path
        self.new = newfilename
        self.error = ErrorType.ok
        self.username = username

    def DocxToPdf(self):
        directory = FILE_FOLDER + self.username
        subprocess.call(['/usr/bin/soffice',
                         '--headless',
                         '--convert-to',
                         'pdf',
                         '--outdir',
                         directory,
                         self.file])
        # delete_path = FILE_FOLDER + '/' + self.file.split('/')[-1]
        # os.remove(delete_path)
        subprocess.call(['mv', self.file.replace('.docx', '.pdf'), directory + '/' + self.new + '.pdf'])
        path = directory + '/' + self.new + '.pdf'
        return path
