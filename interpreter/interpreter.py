# interpreter/interpreter.py

from Myparser.graphml_parser import Node, Edge

def interpret_flowchart(nodes: list[Node], edges: list[Edge], roles: dict, traversal_order: list[str]) -> str:
    id_to_node = {node.id: node for node in nodes}
    edge_map = {(e.source, e.target): (e.label or "").lower() for e in edges}
    next_map = {}  # node.id -> list of (target_id, label)

    for edge in edges:
        if edge.source not in next_map:
            next_map[edge.source] = []
        next_map[edge.source].append((edge.target, (edge.label or "").lower()))

    steps = []
    visited = set()
    step_num = 1

    for node_id in traversal_order:
        if node_id in visited:
            continue
        visited.add(node_id)

        node = id_to_node[node_id]
        label = node.label.strip() if node.label else "Unnamed step"
        role = roles.get(node_id, "Unknown")

        if role == "Start":
            steps.append(f"{step_num}. Start the algorithm.")
        elif role == "End":
            steps.append(f"{step_num}. End the algorithm.")
        elif role == "Input":
            steps.append(f"{step_num}. Ask the user to input: {label}.")
        elif role == "Output":
            steps.append(f"{step_num}. Display the message: {label}.")
        elif role == "Process":
            steps.append(f"{step_num}. Perform the step: {label}.")
        elif role == "Decision":
            steps.append(f"{step_num}. If {label}:")

            yes_target = None
            no_target = None

            for target_id, edge_label in next_map.get(node_id, []):
                if "yes" in edge_label:
                    yes_target = id_to_node.get(target_id)
                elif "no" in edge_label:
                    no_target = id_to_node.get(target_id)

            if yes_target:
                steps.append(f"    - If yes: {yes_target.label.strip()}")
            if no_target:
                steps.append(f"    - If no: {no_target.label.strip()}")

        else:
            steps.append(f"{step_num}. Perform the action: {label}.")

        step_num += 1

    # Final prompt
    prompt = (
        "You are given a flowchart representing an algorithm.\n"
        "Convert the following steps into a valid Python program:\n\n"
        + "\n".join(steps)
    )

    return prompt
