from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import random
import string

def generate_random_string(min_length=1, max_length=8):
    length = random.randint(min_length, max_length)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"<<{random_string}>>"

def create_word_document(num_pages, filename):
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

    for _ in range(num_pages):
        for _ in range(13):
            paragraph = doc.add_paragraph()
            while len(paragraph.text) < 70:
                paragraph.add_run(generate_random_string() + " ")
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        doc.add_page_break()

    if doc.paragraphs[-1].text == '':
        p = doc.paragraphs[-1]._element
        p.getparent().remove(p)

    doc.save(filename)

if __name__ == "__main__":
    create_word_document(100, 'random_text_document.docx')
