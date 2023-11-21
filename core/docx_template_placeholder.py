import re
from docx import Document
from typing import Dict
from constants.variables import *
from constants.msg import ErrorType
from core.pdf_convertor import Convert2PDF
from core.error_block import ErrorBlocker
import os


class DocxTemplatePlaceholder:

    def __init__(self,
                 username: str,
                 template: str,
                 newfilename: str,
                 tags: Dict,
    ):
        self.error = ErrorType.ok
        try:
            # print(os.path.isfile(template))
            # print(os.getcwd())
            # with open("error.txt", "w") as file:
            #     file.write(f"{os.getcwd()}\n")
            self.template_document = Document(template[3:])
            self.file_name = template.split('/')[-1]
            self.replace_tags = self.__prepare_tags(tags)
            self.username = username
            self.new = newfilename
        except Exception as e:
            print("Произошла ошибка:", e)
            self.error = ErrorType.incorrect_doc

    def process(self):
        if self.error:
            return ErrorBlocker().process(self.error)
        try:
            self.__process(self.template_document, self.replace_tags)
            path = FILE_FOLDER + self.username + "/" + self.file_name
            self.template_document.save(path[3:])
            return Convert2PDF(path, self.new, self.username).DocxToPdf()
        except:
            self.error = ErrorType.internal_error
            return ErrorBlocker().process(self.error)

    def __process(self, doc, tags):
        reg = ""
        for p in doc.paragraphs:
            inline = p.runs
            flag = False
            for i in range(len(inline)):
                left = inline[i].text.find("<<")
                left_part = inline[i].text.find("<")
                right = inline[i].text.find(">>")
                right_part = inline[i].text.find(">")
                if left != -1 and right != -1:
                    reg = inline[i].text
                elif left != -1:
                    reg += inline[i].text
                    inline[i].text = ""
                    flag = True
                    continue
                elif right != -1:
                    reg += inline[i].text
                    inline[i].text = ""
                    flag = False
                elif left == -1 and right == -1 and flag:
                    reg += inline[i].text
                    inline[i].text = ""
                    continue
                elif left == -1 and right != -1 and flag:
                    reg += inline[i].text
                    inline[i].text = ""
                elif left_part != -1:
                    if len(inline) > i+1 and inline[i + 1].text[0] == "<":
                        reg += inline[i].text
                        inline[i].text = ""
                        flag = True
                        continue
                    else: continue
                elif right_part != -1:
                    if len(inline) > i+1 and inline[i + 1].text[0] == ">":
                        reg += inline[i].text
                        inline[i].text = ""
                        continue
                    elif reg[-1] == ">":
                        reg += inline[i].text
                        inline[i].text = ""
                    else:
                        continue
                else:
                    continue

                for regex, replace in tags.items():
                    if regex.search(reg):
                        text = regex.sub(replace, reg)
                        inline[i].text = text
                        break
                reg = ""

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.__process(cell, tags)

    def __prepare_tags(self, tags):
        done_tags = dict()
        for regex, replace in tags.items():
            done_tags[re.compile(fr"<<{regex}>>")] = replace
        return done_tags

# DocxTemplatePlaceholder("out_test_files", "./test_files/pdf_test_original.docx", {"name": "idi", "lastname": "na", "data": "hui"}).process()
