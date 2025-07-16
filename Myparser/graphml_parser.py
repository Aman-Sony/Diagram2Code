# parser/graphml_parser.py

import xml.etree.ElementTree as ET

class Node:
    def __init__(self, node_id, label="", shape=""):
        self.id = node_id
        self.label = label
        self.shape = shape

    def __repr__(self):
        return f"Node(id='{self.id}', label='{self.label}', shape='{self.shape}')"

class Edge:
    def __init__(self, source, target, label=""):
        self.source = source
        self.target = target
        self.label = label

    def __repr__(self):
        return f"Edge(source='{self.source}', target='{self.target}', label='{self.label}')"

def parse_graphml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = {
            'graphml': 'http://graphml.graphdrawing.org/xmlns',
            'y': 'http://www.yworks.com/xml/graphml'
        }

        nodes = []
        edges = []

        graph = root.find("graphml:graph", ns)

        if graph is None:
            print("No <graph> element found.")
            return [], []

        for node in graph.findall("graphml:node", ns):
            node_id = node.attrib['id']
            label = ""
            shape = ""

            label_elem = node.find(".//y:NodeLabel", ns)
            if label_elem is not None:
                label = label_elem.text.strip() if label_elem.text else ""

            shape_elem = node.find(".//y:Shape", ns)
            if shape_elem is not None:
                shape = shape_elem.attrib.get("type", "")

            nodes.append(Node(node_id, label, shape))

        for edge in graph.findall("graphml:edge", ns):
            source = edge.attrib['source']
            target = edge.attrib['target']
            label = ""

            label_elem = edge.find(".//y:EdgeLabel", ns)
            if label_elem is not None:
                label = label_elem.text.strip() if label_elem.text else ""

            edges.append(Edge(source, target, label))

        return nodes, edges

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return [], []
