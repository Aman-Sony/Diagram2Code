# classifier/shape_label.py

from Myparser.graphml_parser import Node

def classify_node_roles(nodes: list[Node], diagram_type: str) -> dict:
    node_roles = {}

    for node in nodes:
        label = (node.label or "").strip().lower()
        shape = (node.shape or "").strip().lower()
        role = "Unknown"

        # Handle FLOWCHART
        if diagram_type == "Flowchart":
            if "start" in label or "begin" in label:
                role = "Start"
            elif "end" in label or "stop" in label:
                role = "End"
            elif any(word in label for word in ["input", "read", "enter"]):
                role = "Input"
            elif any(word in label for word in ["output", "print", "display"]):
                role = "Output"
            elif any(word in label for word in ["if", "else", "?", "yes", "no"]):
                role = "Decision"
            elif any(sym in label for sym in ["=", "+", "-", "*", "/", "%", "<", ">", "and", "or"]):
                role = "Process"
            elif shape in ["rectangle", "roundrectangle", "box"]:
                role = "Process"

        # Handle UML
        elif diagram_type == "UML Class Diagram":
            if "class" in label or "<<interface>>" in label or "object" in label:
                role = "Class"
            elif "()" in label or "(" in label and ")" in label:
                role = "Method"
            elif ":" in label or "=" in label or any(w in label for w in ["int", "str", "float", "bool"]):
                role = "Attribute"
            else:
                role = "Unknown UML Part"

        node_roles[node.id] = role

    return node_roles
