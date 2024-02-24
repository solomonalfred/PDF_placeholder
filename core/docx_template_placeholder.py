import os.path
import re
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from typing import Dict

from docx.shared import Pt

from constants.variables import *
from constants.msg import ErrorType
from constants.core_items import *
from core.pdf_convertor import Convert2PDF
from core.error_block import ErrorBlocker


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
        except:
            self.error = ErrorType.incorrect_doc

    def process(self):
        if self.error:
            return ErrorBlocker().process(self.error)
        try:
            self.__process(self.template_document, self.replace_tags)
            self.__placeholder_footer_header()
            tmp_filename = self.file_name.replace(Process_items.DOCX, Process_items.NEW_DOCX)
            path = os.path.join(FILE_FOLDER, self.username, tmp_filename)
            self.template_document.save(path)
            return Convert2PDF(path, self.new, self.username).DocxToPdf()
        except:
            self.error = ErrorType.internal_error
            return ErrorBlocker().process(self.error)

    def __process(self, doc, tags):

        for p in doc.paragraphs:
            inline = p.runs
            flag = False
            table_flag = self.__generate_table(tags[1], p, doc)
            if table_flag: continue
            self.__placeholder_tags(inline, tags[0], flag)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.__process(cell, tags)

    def __generate_table(self, tb, p, doc):
        table_flag = False
        for regex, replace in tb.items():
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
                    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for cell in hdr_cells:
                    self.__set_cell_borders(cell, top=True, bottom=True, left=False, right=False)
                for crypto in replace:
                    row_cells = table.add_row().cells
                    for idx, key in enumerate(keys):
                        row_cells[idx].text = str(crypto[key])
                        self.__set_cell_borders(row_cells[idx], top=True, bottom=True, left=False, right=False)
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.size = Pt(10)
                                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                                self.__set_cell_borders(cell)
                tbl_element = table._tbl
                p_element = p._p
                p_parent = p_element.getparent()
                p_parent.insert(p_parent.index(p_element), tbl_element)
                break
        return table_flag

    def __placeholder_tags(self, inline, tags, flag):
        reg = ""
        for i in range(len(inline)):
            left = inline[i].text.find(Inline.LEFT_BORDER)
            left_part = inline[i].text.find(Inline.PART_LEFT_BORDER)
            right = inline[i].text.find(Inline.RIGHT_BORDER)
            right_part = inline[i].text.find(Inline.PART_RIGHT_BORDER)
            if left != -1 and right != -1: reg = inline[i].text
            elif left != -1:
                reg += inline[i].text
                inline[i].text = ""
                flag = True
                continue
            elif right != -1 and flag:
                reg += inline[i].text
                inline[i].text = reg
                flag = False
            elif left == -1 and right == -1 and flag:
                reg += inline[i].text
                inline[i].text = ""
                continue
            elif left_part != -1:
                if len(inline) > i + 1 and inline[i + 1].text[0] == Inline.PART_LEFT_BORDER:
                    reg += inline[i].text
                    inline[i].text = ""
                    flag = True
                    continue
                else: continue
            elif right_part != -1 and flag:
                if len(inline) > i + 1 and inline[i + 1].text[0] == Inline.PART_RIGHT_BORDER:
                    reg += inline[i].text
                    inline[i].text = ""
                    continue
                elif reg[-1] == Inline.PART_RIGHT_BORDER:
                    reg += inline[i].text
                    inline[i].text = reg
                else:
                    reg += inline[i].text
                    inline[i].text = ""
                    continue
            else: continue
            self.__replace_tags(tags, inline[i], reg)
            reg = ""

    def __replace_tags(self, tags, inline, reg):
        for regex, replace in tags.items():
            if regex.search(reg):
                text = regex.sub(replace, reg)
                inline.text = text
                break

    def __placeholder_footer_header(self):
        for section in self.template_document.sections:
            self.__process(section.header, self.replace_tags)
            self.__process(section.footer, self.replace_tags)

    def __set_cell_borders(self, cell, top=True, bottom=True, left=True, right=True):
        sides = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
        for border in cell._tc.tcPr:
            if border.tag.endswith('tcBorders'):
                for side in border:
                    side.attrib.clear()  # Удаляем все существующие границы
                    side_val = 'single' if sides[side.tag.split('}')[
                        -1]] else 'none'  # Устанавливаем тип границы в зависимости от указанных сторон
                    side.attrib['val'] = side_val
        # sides = [Table_items.TOP,
    #                  Table_items.LEFT,
    #                  Table_items.BOTTOM,
    #                  Table_items.RIGHT]
    #         for side in sides:
    #             border_elm = OxmlElement(Table_items.OXML.format(side))
    #             border_att = {
    #                 f'{qn(Table_items.VALUE)}': Table_items.SINGLE,
    #                 f'{qn(Table_items.SZ)}': str(border_sz),
    #                 f'{qn(Table_items.SPACE)}': Table_items.ZERO,
    #                 f'{qn(Table_items.COLOR)}': Table_items.AUTO,
    #             }
    #             border_elm.attrib.update(border_att)
    #             cell._tc.get_or_add_tcPr().append(border_elm)


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
    data['tables'] = {}
    data["keys"]["hi"] = "Привет"
    data["keys"]["buy"] = "Покеда"
    data["keys"]["name"] = "Laplas"
    data["keys"]["lastname"] = "Solomon"
    data['keys']['data'] = "February"
    data['keys']['satana'] = 'God'

    data['tables']['cryptocurrency_tb'] = [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price_usd": 39857.20,
                "price_eur": 34991.42,
                "price_gbp": 29489.55
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "price_usd": 2845.62,
                "price_eur": 2498.75,
                "price_gbp": 2104.89
            },
            {
                "name": "Ripple",
                "symbol": "XRP",
                "price_usd": 0.84,
                "price_eur": 0.74,
                "price_gbp": 0.62
            }
        ]

    DocxTemplatePlaceholder("out_test_files",
                            "../test_files/footers.docx",
                            "footers",
                            data
                            ).process()
