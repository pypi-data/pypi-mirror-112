"""
Extract, find, or navigate interesting parts of the article (e.g. main content, paragraph)

The extraction should only rely on inspected information (defined in `kiji.inspection`)
and it should avoid using the underline parsed HTML information.
"""

from typing import List, Tuple


from kiji.inspection import InspectedElement, InspectedPage

from collections import deque


def extract_content_element(inspection: InspectedPage) -> InspectedElement:
    # A content is an element with a lot of paragraphs
    max_paragraph_char_count = 0
    max_paragraph_elem = None

    processing_queue = deque([inspection])
    while len(processing_queue) > 0:

        elem = processing_queue.popleft()
        for c in elem.children:
            processing_queue.append(c)

        paragraph_char_count = sum((len(c.get_formatted_text()) for c in elem.children if c.is_paragraph))
        if paragraph_char_count > max_paragraph_char_count:
            max_paragraph_elem = elem
            max_paragraph_char_count = paragraph_char_count

    return max_paragraph_elem


def extract_paragraph_elements(
        element: InspectedElement,
        include_headers=False,
        include_images=False,
) -> List[InspectedElement]:
    paragraphs = []
    if not element.children:
        return paragraphs

    paragraphs = []
    for c in element.children:
        if c.is_inline:
            # Todo: support this later. this is un-expected for now
            continue

        if not c.is_paragraph:
            paragraphs += extract_paragraph_elements(c, include_headers=include_headers)
            continue

        if c.is_header and not include_headers:
            continue

        if c.is_image and not include_images:
            continue

        paragraphs += [c]

    return paragraphs

