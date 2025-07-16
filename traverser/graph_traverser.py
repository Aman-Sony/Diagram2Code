# traverser/graph_traverser.py

from Myparser.graphml_parser import Node, Edge
from collections import defaultdict, deque

def find_start_node(nodes: list[Node]) -> str:
    for node in nodes:
        label = (node.label or "").lower()
        shape = (node.shape or "").lower()
        if "start" in label or shape == "ellipse":
            return node.id
    return nodes[0].id if nodes else None

def build_adjacency(edges: list[Edge]) -> dict:
    adj = defaultdict(list)
    edge_labels = defaultdict(list)

    for edge in edges:
        adj[edge.source].append(edge.target)
        edge_labels[(edge.source, edge.target)] = (edge.label or "").lower()

    return adj, edge_labels

def traverse_graph(nodes: list[Node], edges: list[Edge]) -> list[str]:
    node_map = {node.id: node for node in nodes}
    start_node = find_start_node(nodes)
    if not start_node:
        return []

    adj, edge_labels = build_adjacency(edges)
    visited = set()
    order = []

    queue = deque()
    queue.append(start_node)

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        order.append(current)

        neighbors = adj.get(current, [])
        if len(neighbors) <= 1:
            queue.extend(neighbors)
        else:
            # Branching — follow both yes/no or all branches
            yes_target = None
            no_target = None
            other_targets = []

            for target in neighbors:
                label = edge_labels.get((current, target), "")
                if "yes" in label:
                    yes_target = target
                elif "no" in label:
                    no_target = target
                else:
                    other_targets.append(target)

            if yes_target:
                queue.append(yes_target)
            if no_target:
                queue.append(no_target)
            queue.extend(other_targets)

    return order
