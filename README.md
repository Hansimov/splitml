# SplitML

Split Markup Language (HTML and Markdown) to Groups and Nodes

![](https://img.shields.io/pypi/v/splitml?label=splitml&color=blue)

## Install

```sh
pip install --upgrade splitml
```

## Usage

```python
from splitml import HTMLSplitter, NodesGrouper, stat_tokens

html_root = Path(__file__).parent / "samples"
html_paths = sorted(list(html_root.glob("*.md.html")))[:2]
splitter = HTMLSplitter()
grouper = NodesGrouper()
for html_path in html_paths:
    # print(f"> Processing: {html_path}")
    nodes = splitter.split_html_file(html_path)
    # print(f"  - {len(nodes)} doc nodes.")
    stat_tokens(nodes)
    grouped_nodes = grouper.group_nodes(nodes)
    # print(f"  - {len(grouped_nodes)} doc groups.")
    stat_tokens(grouped_nodes)
```

## Classes

```python
class HTMLSplitter:
    ...

class NodesGrouper:
    ...
```

## Functions

```python
def split_html_str(html_str: str):
    ...

def split_html_file(html_path: Union[Path, str]):
    ...

def chunk_html_str(html_str: str):
    ...

def chunk_html_file(html_path: Union[Path, str]):
    ...
```

```python
def count_tokens(text):
    ...

def stat_tokens(nodes, console_abnormal=False):
    ...
```
