from pathlib import Path

from purehtml import purify_html_files
from tclogger import logger


if __name__ == "__main__":
    html_root = Path(__file__).parent / "samples"
    html_paths = list(html_root.glob("*.html"))
    html_path_and_purified_content_list = purify_html_files(
        html_paths,
        verbose=False,
        output_format="html",
        keep_href=False,
        keep_format_tags=False,
        keep_group_tags=True,
        math_style="latex_in_tag",
    )
    for item in html_path_and_purified_content_list:
        html_path = item["path"]
        purified_content = item["output"]
        output_path = item["output_path"]
        logger.file(output_path.name)
