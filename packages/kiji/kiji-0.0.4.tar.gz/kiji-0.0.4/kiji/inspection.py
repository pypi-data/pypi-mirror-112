"""
Inspect the input and create abstraction/wrapper for HTML/page elements

Instead of accessing the underline library's Element class (currently, BS4's PageElement) directly,
we define a wrapped Element class with additional inspected information (`InspectedElement`)
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Union, Callable

import re

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, PageElement

TAG_NAMES_SKIP = {'script', 'style', 'code', 'svg'}
TAG_NAMES_INLINE = {'a', 'b', 'em', 'i', 'strong', 'span', 'br'}
TAG_NAMES_HEADER = {'h1', 'h2', 'h3', 'h4'}


def inspect(input: Union[str, PageElement]) -> InspectedPage:
    return InspectedPage.from_input(input)


def inspect_file(filename: str) -> InspectedPage:
    with open(filename) as f:
        return inspect(f.read())


def find_element(root: InspectedElement, check_method: Callable[[InspectedElement], bool]) -> Optional[
    InspectedElement]:
    if check_method(root):
        return root

    for c in root.children:
        found_elem = find_element(c, check_method)
        if found_elem:
            return found_elem

    return None


class InspectedElement:

    def __init__(self,
                 element: PageElement,
                 is_inline: bool,
                 parent: Optional[InspectedElement],
                 children: List[InspectedElement]):
        self._element = element
        self._is_inline: bool = is_inline
        self._parent: Optional[InspectedElement] = parent
        self._children: List[InspectedElement] = children

    @staticmethod
    def from_page_element(node: PageElement, parent: Optional[InspectedElement] = None) -> Optional[InspectedElement]:

        if isinstance(node, NavigableString):
            if not str(node).strip():
                return None

            return InspectedElement(node, True, parent, [])

        assert isinstance(node, Tag)
        if node.name in TAG_NAMES_SKIP:
            return None


        result = InspectedElement(
            node,
            node.name in TAG_NAMES_INLINE,
            parent,
            []
        )

        all_children_inline = True
        all_children_results = []
        for child_node in node.contents:
            child_node_inspection = InspectedElement.from_page_element(child_node, parent=result)
            if child_node_inspection:
                all_children_inline &= child_node_inspection.is_inline
                all_children_results.append(child_node_inspection)

        result._is_inline = result._is_inline and all_children_inline
        result._children = all_children_results
        return result

    @property
    def is_inline(self):
        return self._is_inline

    @property
    def is_paragraph(self):
        return not self._is_inline and all((c.is_inline for c in self._children))

    @property
    def is_header(self):
        return self.is_paragraph and self._element_name() in TAG_NAMES_HEADER

    @property
    def is_image(self):
        return self._element_name() == 'img'

    @property
    def children(self):
        return self._children

    @property
    def is_element(self):
        return isinstance(self._element, Tag)

    def get_formatted_text(self):
        if not self._children:
            return self._element_text()

        lines = ['']
        for c in self._children:
            if c._element_name() in {'br'}:
                lines[-1] += '\n'
                continue

            if c.is_inline:
                lines[-1] += c.get_formatted_text()
                continue

            lines += [c.get_formatted_text()]

        lines = [l for l in lines if l.strip()]
        return '\n'.join(lines)

    def get_formatted_html(self):
        if isinstance(self._element, NavigableString):
            return self._element_text()

        if self.is_inline:
            inner_html = [c.get_formatted_html() for c in self._children]
            inner_html = ''.join(inner_html)
            tag = self._element_name()

            if inner_html:
                return f'<{tag}>{inner_html}</{tag}>'
            else:
                return f'<{tag}/>'

        return '\n'.join(self._get_formatted_html_lines())

    def _get_formatted_html_lines(self) -> List[str]:
        assert not self._is_inline
        assert isinstance(self._element, Tag)

        lines = ['']
        for c in self._children:
            if c.is_inline:
                lines[-1] += c.get_formatted_html()
            else:
                lines += c._get_formatted_html_lines()
                lines += ['']

        lines = [l for l in lines if l.strip()]
        if len(lines) == 1:
            return [f'<{self._element.name}>' + lines[0] + f'</{self._element.name}>']

        return [f'<{self._element.name}>'] + \
               ['\t' + l for l in lines if l] + \
               [f'</{self._element.name}>']

    def _element_text(self):
        if isinstance(self._element, NavigableString):
            text = str(self._element)
        else:
            assert isinstance(self._element, Tag)
            text = self._element.text
        return re.sub('\\s+', ' ', text)

    def _element_class(self) -> Optional[List[str]]:
        if isinstance(self._element, Tag):
            return self._element['class']
        else:
            return None

    def _element_name(self) -> Optional[str]:
        if isinstance(self._element, Tag):
            return self._element.name
        else:
            return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        node = self._element
        if isinstance(node, NavigableString):
            return f'<ElementInspection TextNode - "{node[:10]}">'

        assert isinstance(node, Tag)
        return f'<ElementInspection[{node.name}]>'


class InspectedPage(InspectedElement):

    @staticmethod
    def from_input(input: Union[str, PageElement]) -> InspectedPage:
        page_elem = _to_page_element(input)

        body = page_elem.find('body')
        if body:
            page_elem = body

        # TODO: More inspection
        page_inspection = InspectedElement.from_page_element(page_elem)

        return InspectedPage(
            page_inspection._element,
            page_inspection.is_inline,
            None,
            page_inspection.children
        )


def _to_page_element(input: Union[str, Tag]) -> Tag:
    if isinstance(input, Tag):
        return input

    if isinstance(input, str):
        return BeautifulSoup(input, 'html.parser')

    raise ValueError(f'Unknown type "${type(input)}" for input ${str(input)}')
