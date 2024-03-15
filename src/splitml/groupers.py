from typing import Literal
from .stats import count_tokens


class NodesGrouper:
    def group_nodes_by_order(
        self,
        nodes,
        max_tokens: list[int] = [128, 256, 512, 1024, 2048],
        overlap_node_count: int = 1,
    ):
        groups = []
        for max_token in max_tokens:
            group = []
            for idx, node in enumerate(nodes):
                node_tokens = node["text_tokens"]
                group_tokens = sum([nd["text_tokens"] for nd in group])
                if group_tokens + node_tokens > max_token:
                    groups.append(group)
                    group = []
                group.append(node)
            if group:
                groups.append(group)

        return groups

    def combine_groups(self, groups):
        grouped_nodes = []
        for group in groups:
            text = "\n\n".join([node["text"] for node in group])
            html = "\n\n".join([node["html"] for node in group])
            group_tokens = count_tokens(text)
            node_idxs = [node["node_idx"] for node in group]
            grouped_nodes.append(
                {
                    "html": html,
                    "text": text,
                    "tag_type": "grouped",
                    "html_len": len(html),
                    "text_len": len(text),
                    "text_tokens": group_tokens,
                    "element_idxs": node_idxs,
                }
            )
        return grouped_nodes

    def group_nodes(
        self,
        nodes,
        max_tokens: list[int] = [128, 256, 512, 1024, 2048],
    ):
        groups = self.group_nodes_by_order(nodes, max_tokens=max_tokens)
        grouped_nodes = self.combine_groups(groups)
        return grouped_nodes
