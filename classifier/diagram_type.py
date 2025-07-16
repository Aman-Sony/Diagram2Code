# classifier/diagram_type.py

from Myparser.graphml_parser import Node

def classify_diagram_type(nodes: list[Node]) -> str:
    uml_keywords = ['class', 'attribute', 'method', '<<interface>>']
    flowchart_keywords = ['start', 'stop', 'input', 'output', 'decision', 'process']
    uml_shapes = ['rectangle', 'roundrectangle']
    flowchart_shapes = ['ellipse', 'diamond', 'parallelogram', 'hexagon', 'rectangle', 'roundrectangle']

    uml_score = 0
    flow_score = 0

    for node in nodes:
        label = (node.label or "").lower()
        shape = (node.shape or "").lower()

        # Score for UML based on label
        if any(kw in label for kw in uml_keywords):
            uml_score += 2

        # Score for flowchart based on label
        if any(kw in label for kw in flowchart_keywords):
            flow_score += 2

        # Score based on shape type
        if shape in uml_shapes:
            uml_score += 1
        if shape in flowchart_shapes:
            flow_score += 1

    # Decision logic
    if uml_score > flow_score + 2:
        return "UML Class Diagram"
    elif flow_score > uml_score + 2:
        return "Flowchart"
    else:
        return "Unknown"
