import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
from dowhy import CausalModel
import tempfile
import os

# -- Helper Functions --
def visualize_dag(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    net = Network(height="500px", width="100%", directed=True)
    for node in nodes:
        net.add_node(node, label=node)
    for src, tgt in edges:
        net.add_edge(src, tgt)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)
    return tmp_file.name

def run_dowhy_analysis(df, edges, treatment, outcome):
    dot_str = "digraph {\n"
    for src, tgt in edges:
        dot_str += f"    {src} -> {tgt};\n"
    dot_str += "}"

    model = CausalModel(
        data=df,
        treatment=treatment,
        outcome=outcome,
        graph=dot_str
    )

    identified_estimand = model.identify_effect()
    estimate = model.estimate_effect(identified_estimand,
                                     method_name="backdoor.linear_regression")
    return estimate

# -- Streamlit App --
st.set_page_config(page_title="CausalIQ - No-Code Causal Inference")
st.title("CausalIQ - No-Code Causal Inference Platform")

st.sidebar.header("1. Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview of Uploaded Data")
    st.write(df.head())

    all_cols = df.columns.tolist()

    st.sidebar.header("2. Define Causal Graph (DAG)")
    nodes = st.sidebar.multiselect("Select variables (nodes)", all_cols, default=all_cols)

    edges = []
    st.sidebar.markdown("### Add Edges (Cause → Effect)")
    for i in range(3):
        src = st.sidebar.selectbox(f"Edge {i+1} - Source", nodes, key=f"src_{i}")
        tgt = st.sidebar.selectbox(f"Edge {i+1} - Target", nodes, key=f"tgt_{i}")
        if src != tgt:
            edges.append((src, tgt))

    if edges:
        st.subheader("🔗 Visualized DAG")
        dag_path = visualize_dag(nodes, edges)
        with open(dag_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=500)
        os.remove(dag_path)

        st.sidebar.header("3. Select Treatment and Outcome")
        treatment = st.sidebar.selectbox("Select Treatment Variable", nodes)
        outcome = st.sidebar.selectbox("Select Outcome Variable", [col for col in nodes if col != treatment])

        if st.sidebar.button("🔍 Estimate Causal Effect"):
            with st.spinner("Running DoWhy Analysis..."):
                estimate = run_dowhy_analysis(df, edges, treatment, outcome)
                st.subheader("📈 Estimated Causal Effect")
                st.write(estimate)
                st.success("Analysis Complete!")