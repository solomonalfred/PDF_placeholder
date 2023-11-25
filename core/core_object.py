from typing import Dict, Any
from .docx_template_placeholder import DocxTemplatePlaceholder


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
