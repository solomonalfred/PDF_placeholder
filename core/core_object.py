from typing import Dict, Any
from .docx_template_placeholder import DocxTemplatePlaceholder


class Core:

    def __init__(self, username: str, file: Any, regex: Dict):
        self.username = username
        self.template = file
        self.tags = regex

    def process(self):
        return DocxTemplatePlaceholder(self.username, self.template, self.tags).process()
