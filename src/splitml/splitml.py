from pathlib import Path

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

    def split_html_str(self, html_str):
        results = []
        soup = BeautifulSoup(html_str, "html.parser")
        for idx, element in enumerate(soup.find_all(SPLIT_TAGS, recursive=False)):
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

    def split_html_file(self, html_path):
        html_str = self.read_html_file(html_path)
        return self.split_html_str(html_str)


def split_html_str(html_str):
    splitter = HTMLSplitter()
    return splitter.split_html_str(html_str)


def split_html_file(html_path):
    splitter = HTMLSplitter()
    return splitter.split_html_file(html_path)


if __name__ == "__main__":
    html_root = Path(__file__).parent / "samples"
    html_paths = list(html_root.glob("*.md.html"))
    splitter = HTMLSplitter()
    grouper = NodesGrouper()
    for html_path in html_paths:
        logger.note(f"Processing: {html_path}")
        nodes = splitter.split_html_file(html_path)
        # pprint(nodes, width=150, sort_dicts=False)
        logger.success(f"{len(nodes)} doc nodes.")
        stat_tokens(nodes)
        grouped_nodes = grouper.group_nodes(nodes)
        logger.success(f"{len(grouped_nodes)} doc groups.")
        stat_tokens(grouped_nodes)

    # python -m splitml.splitml
