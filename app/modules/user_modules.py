import shutil
import os
from constants.variables import *
from fastapi import UploadFile, File
from docx import Document
import re
import PyPDF2


def save_file(username: str, input_file_data: UploadFile = File(...)):
    try:
        # str(uuid.uuid4())[:8] + '_' +
        filename = input_file_data.filename
        path = os.path.join(FILE_FOLDER + username, filename)
        with open(f'{path}', "wb") as buffer:
            shutil.copyfileobj(input_file_data.file, buffer)
        return path
    except:
        return ''

def get_tags(file_path: str):
    tags = []
    pattern = r"<<(.*?)>>"
    def process(doc):
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
                    if len(inline) > i + 1 and inline[i + 1].text[0] == "<":
                        reg += inline[i].text
                        inline[i].text = ""
                        flag = True
                        continue
                    else:
                        continue
                elif right_part != -1:
                    if len(inline) > i + 1 and inline[i + 1].text[0] == ">":
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
                matches = re.findall(pattern, reg)
                for match in matches:
                    tags.append(match)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    process(cell)

    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, "../../tags.txt")
    with open(file, "w") as file:
        #         file.write(f"{os.getcwd()}\n")
        #         file.write(f"{file_path}\n")
        #         file.write(f"{os.path.isfile(file_path)}\n")
        try:
            doc = Document(file_path)
            process(doc)
            file.write("Tags: correct document\n")
        except:
            file.write("Tags error: incorrect document\n")

    return list(set(tags))

def dict_tags(tags):
    tag = {}
    for i in tags:
        tag[i] = ""
    return tag

def transform_user(old: dict, new: dict):
    old.update(new)
    return old

def delete_transform(old: dict, new: dict):
    if len(old) == 1 and old.get(new['key']) is not None:
        return {}
    if len(old) == 1 and old.get(new['key']) is None:
        return old
    del old[new['key']]
    return old

def count_pages(path: str):
    pdf_file = open(path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    pdf_file.close()
    return num_pages
