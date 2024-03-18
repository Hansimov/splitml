from typing import Literal
from .stats import count_tokens


class NodesGrouper:
    DEFAULT_MAX_TOKENS = [128, 512, 1024]
    DEFAULT_OVERLAP_NODE_COUNT = 1

    def group_nodes_by_order(
        self,
        nodes,
        max_tokens: list[int] = DEFAULT_MAX_TOKENS,
        overlap_node_count: int = DEFAULT_OVERLAP_NODE_COUNT,
    ):
        groups = []
        for max_token in max_tokens:
            group = []
            for idx, node in enumerate(nodes):
                node_tokens = node["text_tokens"]
                group_tokens = sum([nd["text_tokens"] for nd in group])
                if group_tokens + node_tokens > max_token:
                    groups.append(group)
                    if overlap_node_count > 0:
                        group = group[-overlap_node_count:]
                    else:
                        group = []
                group.append(node)
            if group:
                groups.append(group)

        return groups

    def combine_groups(self, groups):
        grouped_nodes = []
        node_idxs_list = []
        for group in groups:
            text = "\n\n".join([node["text"] for node in group])
            html = "\n\n".join([node["html"] for node in group])
            group_tokens = count_tokens(text)
            node_idxs = [node["node_idx"] for node in group]
            node_tags = [node["tag"] for node in group]
            if node_idxs in node_idxs_list:
                continue
            else:
                node_idxs_list.append(node_idxs)
            grouped_nodes.append(
                {
                    "html": html,
                    "text": text,
                    "html_len": len(html),
                    "text_len": len(text),
                    "text_tokens": group_tokens,
                    "node_idxs": node_idxs,
                    "node_tags": node_tags,
                }
            )

        return grouped_nodes

    def group_nodes(
        self,
        nodes,
        max_tokens: list[int] = DEFAULT_MAX_TOKENS,
        overlap_node_count: int = DEFAULT_OVERLAP_NODE_COUNT,
    ):
        groups = self.group_nodes_by_order(
            nodes, max_tokens=max_tokens, overlap_node_count=overlap_node_count
        )
        grouped_nodes = self.combine_groups(groups)
        return grouped_nodes
