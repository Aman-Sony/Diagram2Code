import sys
import os
import streamlit as st

# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Myparser.graphml_parser import parse_graphml
from classifier.diagram_type import classify_diagram_type
from classifier.shape_label import classify_node_roles
from traverser.graph_traverser import traverse_graph
from interpreter.interpreter import interpret_flowchart
from llm.gemini_client import generate_code_with_gemini, list_available_gemini_models

# Session state setup
if "parsed" not in st.session_state:
    st.session_state.parsed = False
    st.session_state.code = ""
    st.session_state.prompt = ""
    st.session_state.diagram_type = ""
    st.session_state.nodes = []
    st.session_state.edges = []
    st.session_state.roles = {}
    st.session_state.order = []

# Sidebar navigation
st.set_page_config(page_title="Diagram2Code", layout="wide")
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Parsed Nodes", "Parsed Edges", "Node Roles", "Execution Order", "Prompt", "Available Models"])

st.title("🧠 Diagram2Code")

# Page: Home
if page == "Home":
    st.subheader("🚀 Start by Uploading Your Diagram")

    diagrams_dir = "diagrams"
    files = [f for f in os.listdir(diagrams_dir) if f.endswith(".graphml")]

    if not files:
        st.warning("No .graphml files found in the 'diagrams/' folder.")
    else:
        selected_file = st.selectbox("Select a .graphml file to parse:", files)

        if st.button("Parse Diagram"):
            full_path = os.path.join(diagrams_dir, selected_file)
            nodes, edges = parse_graphml(full_path)
            diagram_type = classify_diagram_type(nodes)
            roles = classify_node_roles(nodes, diagram_type)
            order = traverse_graph(nodes, edges)
            prompt = interpret_flowchart(nodes, edges, roles, order)

            st.session_state.nodes = nodes
            st.session_state.edges = edges
            st.session_state.roles = roles
            st.session_state.diagram_type = diagram_type
            st.session_state.order = order
            st.session_state.prompt = prompt
            st.session_state.parsed = True
            st.session_state.code = ""

        if st.session_state.parsed:
            st.subheader("💡 Generated Python Code")
            if st.button("Generate Python Code with Gemini"):
                with st.spinner("Calling Gemini..."):
                    code = generate_code_with_gemini(st.session_state.prompt, model_name="models/gemini-1.5-pro-latest")
                    st.session_state.code = code

            if st.session_state.code:
                st.code(st.session_state.code, language="python")

# Page: Parsed Nodes
elif page == "Parsed Nodes":
    st.subheader("📦 Parsed Nodes")
    if st.session_state.nodes:
        for n in st.session_state.nodes:
            st.markdown(f"- **ID**: `{n.id}` | **Label**: `{n.label}` | **Shape**: `{n.shape}`")
    else:
        st.info("No nodes found.")

# Page: Parsed Edges
elif page == "Parsed Edges":
    st.subheader("🔗 Parsed Edges")
    if st.session_state.edges:
        for e in st.session_state.edges:
            st.markdown(f"- **From**: `{e.source}` → **To**: `{e.target}` | **Label**: `{e.label}`")
    else:
        st.info("No edges found.")

# Page: Node Roles
elif page == "Node Roles":
    st.subheader("🧩 Node Roles")
    for n in st.session_state.nodes:
        role = st.session_state.roles.get(n.id, "Unknown")
        st.markdown(f"- **Label**: `{n.label}` | **Shape**: `{n.shape}` → **Role**: **{role}**")

# Page: Execution Order
elif page == "Execution Order":
    st.subheader("🧭 Traversed Execution Order")
    id_to_label = {n.id: n.label for n in st.session_state.nodes}
    for i, node_id in enumerate(st.session_state.order, 1):
        label = id_to_label.get(node_id, "Unknown")
        st.markdown(f"{i}. **{label}**")

# Page: Prompt
elif page == "Prompt":
    st.subheader("🧠 LLM Prompt")
    st.code(st.session_state.prompt, language="text")

# Page: Available Models
elif page == "Available Models":
    st.subheader("📋 Gemini Models Available to Your API Key")
    if st.button("🔍 Show Available Models"):
        model_list_output = list_available_gemini_models()
        st.code(model_list_output)

