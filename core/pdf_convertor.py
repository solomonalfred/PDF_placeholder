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
        self.file = file_path
        self.new = newfilename
        self.username = username

    def DocxToPdf(self):
        directory = FILE_FOLDER + "volumes/" + self.username
        if os.path.isdir(directory) == False:
            return ErrorBlocker().process(ErrorType.missing_doc)
        subprocess.call(['/usr/bin/soffice',
                         '--headless',
                         '--convert-to',
                         'pdf',
                         '--outdir',
                         directory,
                         self.file])
        os.remove(self.file)
        old = self.file.replace('_new.docx', '_new.pdf')
        new = directory + '/' + self.new + '.pdf'
        subprocess.call(['mv', old, new])
        if os.path.exists(new):
            return new
        return ErrorBlocker().process(ErrorType.missing_doc)
