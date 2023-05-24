from lxml.html.clean import clean_html
from markdown import Markdown


def convert_md_to_html(raw_markdown_text: str) -> str:
    markdowner = Markdown(extensions=["tables", "footnotes", "toc"])
    html = markdowner.convert(raw_markdown_text)
    result = clean_html(html)
    if isinstance(result, str):
        return result
    raise Exception("Bad cleaning.")
