class Inline:
    LEFT_BORDER = "<<"
    RIGHT_BORDER = ">>"
    PART_LEFT_BORDER = "<"
    PART_RIGHT_BORDER = ">"


class Table_items:
    TOP = 'top'
    LEFT = 'left'
    BOTTOM = 'bottom'
    RIGHT = 'right'

    OXML = 'w:{}'
    AUTO = 'auto'
    ZERO = '0'
    SINGLE = 'single'

    VALUE = "w:val"
    SZ = "w:sz"
    SPACE = "w:space"
    COLOR = "w:color"

    TABLE_GRID = 'Table Grid'


class Process_items:
    DOCX = '.docx'
    NEW_DOCX = '_new.docx'

    KEYS = "keys"
    TABLES = "tables"

    REGEX_FORM = r"<<{}>>"


class PDF_items:
    PDF = '.pdf'
    PDF_TMP = '_new.pdf'
    MOVE = 'mv'


PDF_CONVERT = ['/usr/bin/soffice', '--headless', '--convert-to', 'pdf', '--outdir', "", ""]


