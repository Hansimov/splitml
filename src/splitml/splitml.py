from pathlib import Path

from bs4 import BeautifulSoup
from pprint import pprint
from tclogger import logger

BODY_TAGS = ["html", "body"]
GROUP_TAGS = ["div", "section", "p"]
HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
TABLE_TAGS = ["table"]
LIST_TAGS = ["ul", "ol"]
DEF_TAGS = ["dl"]
CODE_TAGS = ["pre", "code"]
MATH_TAGS = ["math"]

SPLIT_TAGS = [
    *BODY_TAGS,
    *GROUP_TAGS,
    *HEADER_TAGS,
    *TABLE_TAGS,
    *LIST_TAGS,
    *DEF_TAGS,
    *CODE_TAGS,
    *MATH_TAGS,
]

TAG_TYPE_MAP = {
    "body": BODY_TAGS,
    "group": GROUP_TAGS,
    "header": HEADER_TAGS,
    "table": TABLE_TAGS,
    "list": LIST_TAGS,
    "def": DEF_TAGS,
    "code": CODE_TAGS,
    "math": MATH_TAGS,
}


class HTMLSplitter:
    def get_tag_type(self, element):
        tag_type = ""
        for key, tags in TAG_TYPE_MAP.items():
            if element.name in tags:
                tag_type = key
                break
        return tag_type

    def read_html_file(self, html_path):
        if not Path(html_path).exists():
            warn_msg = f"File not found: {html_path}"
            logger.warn(warn_msg)
            raise FileNotFoundError(warn_msg)

        encodings = ["utf-8", "latin-1"]
        for encoding in encodings:
            try:
                with open(html_path, "r", encoding=encoding, errors="ignore") as rf:
                    html_str = rf.read()
                    return html_str
            except UnicodeDecodeError:
                pass
        else:
            warn_msg = f"No matching encodings: {html_path}"
            logger.warn(warn_msg)
            raise UnicodeDecodeError(warn_msg)

    def split_html_file(self, html_path):
        results = []
        html_str = self.read_html_file(html_path)
        soup = BeautifulSoup(html_str, "html.parser")
        for element in soup.find_all(SPLIT_TAGS):
            element_str = str(element)
            item = {
                "tag": element.name,
                "tag_type": self.get_tag_type(element),
                "html": element_str,
                "length": len(element_str),
            }
            logger.success(f"Found element: {element.name}")
            results.append(item)

        for item in results:
            pprint(item, width=120)
        return results


if __name__ == "__main__":
    html_root = Path(__file__).parent / "samples"
    html_paths = list(html_root.glob("*.md.html"))
    splitter = HTMLSplitter()
    for html_path in html_paths:
        logger.note(f"Processing: {html_path}")
        splitter.split_html_file(html_path)
    # python -m splitml.splitml
