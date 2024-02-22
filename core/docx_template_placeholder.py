import re
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
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
                 tags: Dict
    ):
        self.error = ErrorType.ok
        try:
            self.template_document = Document(template)
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
            for section in self.template_document.sections:
                header = section.header
                self.__process(header, self.replace_tags)
                footer = section.footer
                self.__process(footer, self.replace_tags)
            path = (FILE_FOLDER + "volumes/" + self.username + "/"
                    + self.file_name.replace('.docx', '_new.docx'))
            self.template_document.save(path)
            return Convert2PDF(path, self.new, self.username).DocxToPdf()
        except Exception as e:
            print("Произошла ошибка:", e)
            self.error = ErrorType.internal_error
            return ErrorBlocker().process(self.error)

    def __process(self, doc, tags):
        reg = ""
        for p in doc.paragraphs:
            inline = p.runs
            flag = False
            table_flag = False
            for regex, replace in tags[1].items():
                if regex.search(p.text):
                    table_flag = True
                    p.text = ''
                    num_columns = len(replace[0])
                    table = doc.add_table(rows=1, cols=num_columns)
                    hdr_cells = table.rows[0].cells
                    keys = list(replace[0].keys())
                    for i in range(num_columns):
                        paragraph = hdr_cells[i].paragraphs[0]
                        run = paragraph.add_run(keys[i].capitalize().replace('_', ' '))
                        run.bold = True
                    for cell in hdr_cells:
                        self.__set_cell_borders(cell, border_sz=8)
                    for crypto in replace:
                        row_cells = table.add_row().cells
                        for idx, key in enumerate(keys):
                            row_cells[idx].text = str(crypto[key])
                            self.__set_cell_borders(row_cells[idx], border_sz=8)
                    tbl_element = table._tbl
                    p_element = p._p
                    p_parent = p_element.getparent()
                    p_parent.insert(p_parent.index(p_element) + 1, tbl_element)
                    break
            if table_flag: continue
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
                    inline[i].text = reg
                    flag = False
                elif left == -1 and right == -1 and flag:
                    reg += inline[i].text
                    inline[i].text = ""
                    continue
                elif left == -1 and right != -1 and flag:
                    reg += inline[i].text
                    inline[i].text = reg
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
                        inline[i].text = reg
                    else:
                        continue
                else:
                    continue

                for regex, replace in tags[0].items():
                    if regex.search(reg):
                        text = regex.sub(replace, reg)
                        inline[i].text = text
                        break

                reg = ""

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.__process(cell, tags)

    def __set_cell_borders(self, cell, border_sz=4):
        sides = ['top', 'left', 'bottom', 'right']
        for side in sides:
            border_elm = OxmlElement(f'w:{side}')
            border_att = {
                f'{qn("w:val")}': 'single',
                f'{qn("w:sz")}': str(border_sz),
                f'{qn("w:space")}': '0',
                f'{qn("w:color")}': 'auto',
            }
            border_elm.attrib.update(border_att)
            cell._tc.get_or_add_tcPr().append(border_elm)

    def __prepare_tags(self, tags):
        done_tags = dict()
        done_tb = dict()
        if len(tags.items()) == 0: return [done_tags, done_tb]
        if tags.get("keys") is not None:
            for regex, replace in tags["keys"].items():
                done_tags[re.compile(fr"<<{regex}>>")] = replace
        tb_flag = tags.get("tables")
        if tb_flag is None:
            return [done_tags, done_tb]
        for regex, replace in tags["tables"].items():
            done_tb[re.compile(fr"<<{regex}>>")] = replace
        return [done_tags, done_tb]

if __name__ == "__main__":
    data = {}
    data['keys'] = {}
    # data['tables'] = {}
    data["keys"]["hi"] = "Привет"
    data["keys"]["buy"] = "Покеда"
    data["keys"]["name"] = "Laplas"
    data["keys"]["lastname"] = "Solomon"
    data['keys']['data'] = "February"
    data['keys']['satana'] = 'God'

    # data['tables']['cryptocurrency_tb'] = [
    #         {
    #             "name": "Bitcoin",
    #             "symbol": "BTC",
    #             "price_usd": 39857.20,
    #             "price_eur": 34991.42,
    #             "price_gbp": 29489.55
    #         },
    #         {
    #             "name": "Ethereum",
    #             "symbol": "ETH",
    #             "price_usd": 2845.62,
    #             "price_eur": 2498.75,
    #             "price_gbp": 2104.89
    #         },
    #         {
    #             "name": "Ripple",
    #             "symbol": "XRP",
    #             "price_usd": 0.84,
    #             "price_eur": 0.74,
    #             "price_gbp": 0.62
    #         }
    #     ]

    DocxTemplatePlaceholder("out_test_files",
                            "../test_files/footers.docx",
                            "footers",
                            data
                            ).process()

