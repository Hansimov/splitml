from .stats import count_tokens


class NodesGrouper:
    def group_nodes_by_order(self, nodes, max_tokens=1024, min_tokens=100):
        groups = []
        group = []
        for idx, node in enumerate(nodes):
            node_tokens = node["text_tokens"]
            group_tokens = sum([nd["text_tokens"] for nd in group])
            if group_tokens + node_tokens > max_tokens:
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
            group_tokens = sum([node["text_tokens"] for node in group])
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

    def group_nodes(self, nodes, max_tokens=1024, min_tokens=100):
        groups = self.group_nodes_by_order(nodes, max_tokens, min_tokens)
        grouped_nodes = self.combine_groups(groups)
        return grouped_nodes
