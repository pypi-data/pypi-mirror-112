"""
Kiji's models (Article, Paragraph, ...)

The models should only rely on inspected information (defined in `kiji.inspection`)
and it should NOT use any underline parsed HTML information.
"""

from typing import List, Optional

from kiji.extraction import extract_content_element, extract_paragraph_elements
from kiji.inspection import InspectedPage, InspectedElement, inspect


class Paragraph:
    def __init__(self, element: InspectedElement):
        self.element = element

    @property
    def text(self):
        return self.element.get_formatted_text()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text


class Article:

    def __init__(self, html_input):
        self.page_inspection: InspectedPage = inspect(html_input)
        self.content_element: InspectedElement = extract_content_element(self.page_inspection)

    def get_paragraphs(self,
                       include_headers=False,
                       include_images=False) -> List[Paragraph]:
        paragraph_elements = extract_paragraph_elements(self.content_element, include_headers=include_headers)
        return [Paragraph(elem) for elem in paragraph_elements]

    def to_text(self) -> str:
        pass

    def to_markdown(self) -> str:
        pass

