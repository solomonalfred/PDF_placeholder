from typing import Dict, Any
from core.docx_template_placeholder import DocxTemplatePlaceholder


class Core:

    def __init__(self,
                 username: str,
                 file: str,
                 newfilename: str,
                 regex: Dict
    ):
        self.username = username
        self.template = file
        self.tags = regex
        self.new = newfilename

    def process(self):
        return DocxTemplatePlaceholder(self.username, self.template, self.new, self.tags).process()


if __name__ == "__main__":
    data = {"hi": "Привет",
            "name": "Nikita",
            "lastname": "Bogdanov",
            "data": "23.12",
            "buy": "Пока"}
    Core("out_test_files", "../test_files/footers.docx", "out", data).process()
