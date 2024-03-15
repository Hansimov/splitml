import markdown2

from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup
from pprint import pprint
from purehtml import purify_html_str
from tclogger import logger

from .constants import SPLIT_TAGS, TAG_TYPE_MAP
from .stats import count_tokens, stat_tokens
from .groupers import NodesGrouper


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

    def is_atomized(self, element):
        # check if any children of element has tag in SPLIT_TAGS
        for child in element.descendants:
            if child.name in SPLIT_TAGS:
                return False
        return True

    def md2html(self, md_str):
        return markdown2.markdown(md_str)

    def check_format(func):
        def wrapper(self, html_str, format=None):
            if format == "markdown":
                html_str = self.md2html(html_str)
            format = "html"
            return func(self, html_str, format)

        return wrapper

    @check_format
    def split_html_str(self, html_str, format=None):
        results = []
        soup = BeautifulSoup(html_str, "html.parser")
        for idx, element in enumerate(soup.find_all(SPLIT_TAGS)):
            if not self.is_atomized(element):
                continue
            element_str = str(element)
            markdown_str = purify_html_str(
                element_str,
                output_format="markdown",
                keep_format_tags=False,
                keep_group_tags=False,
                math_style="latex",
            )
            item = {
                "html": element_str,
                "text": markdown_str,
                "tag": element.name,
                "tag_type": self.get_tag_type(element),
                "html_len": len(element_str),
                "text_len": len(markdown_str),
                "text_tokens": count_tokens(markdown_str),
                "node_idx": idx,
            }
            results.append(item)

        return results

    def split_html_file(self, html_path, format=None):
        ext = Path(html_path).suffix
        if not format:
            if ext == ".md":
                format = "markdown"
            else:
                format = "html"
        else:
            format = format

        html_str = self.read_html_file(html_path)
        return self.split_html_str(html_str, format=format)


def split_html_str(html_str: str, format=None):
    return HTMLSplitter().split_html_str(html_str, format=format)


def split_html_file(html_path: Union[Path, str], format=None):
    return HTMLSplitter().split_html_file(html_path, format=format)


def chunk_html_str(html_str: str, format=None):
    nodes = HTMLSplitter().split_html_str(html_str, format=format)
    grouped_nodes = NodesGrouper().group_nodes(nodes)
    return grouped_nodes


def chunk_html_file(html_path: Union[Path, str], format=None):
    nodes = HTMLSplitter().split_html_file(html_path, format=format)
    grouped_nodes = NodesGrouper().group_nodes(nodes)
    return grouped_nodes


if __name__ == "__main__":
    html_root = Path(__file__).parent / "samples"

    file_pattern = "*.html.md"
    html_paths = sorted(
        list(html_root.glob(file_pattern)),
        key=lambda x: str(x).lower(),
    )[:2]
    splitter = HTMLSplitter()
    grouper = NodesGrouper()
    for html_path in html_paths:
        logger.note(f"> Processing: {html_path.name}")
        nodes = splitter.split_html_file(html_path)
        logger.success(f"  - {len(nodes)} nodes.")
        stat_tokens(nodes)
        grouped_nodes = grouper.group_nodes(nodes)
        logger.success(f"  - {len(grouped_nodes)} grouped nodes.")
        stat_tokens(grouped_nodes)

    # python -m splitml.splitml
