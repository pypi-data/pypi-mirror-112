from kiji.article import Article


def from_url(url: str) -> Article:
    pass


def from_file(filename: str) -> Article:
    with open(filename) as f:
        return from_html(f.read())


def from_html(html_input: str) -> Article:
    return Article(html_input)
