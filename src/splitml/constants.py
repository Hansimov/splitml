BODY_TAGS = ["html", "body"]
GROUP_TAGS = ["div", "section", "p"]
HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
TABLE_TAGS = ["table"]
LIST_TAGS = ["ul", "ol", "li"]
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
