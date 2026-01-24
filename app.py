import os
import os
import json
import time
import streamlit as st
from pyvis.network import Network
from dotenv import load_dotenv
import streamlit.components.v1 as components
from io import StringIO
import base64

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Roadmap Generator", layout="wide")
st.sidebar.header("🎧 Customization")
topic = st.sidebar.text_input("📚 Enter Topic", value="Machine Learning")
node_color = st.sidebar.color_picker("🎨 Node Color", "#ADD8E6")
edge_color = st.sidebar.color_picker("🔗 Edge Color", "#FF5733")
node_size = st.sidebar.slider("🔵 Node Size", 10, 100, 34)
font_size = st.sidebar.slider("🌠 Font Size", 10, 40, 30)
layout_type = st.sidebar.selectbox("🧲 Layout", ["repulsion", "barnes_hut"])

st.title("Using NLP and LLM/Model Roadmap Generator 🚀")
st.write("Generate a roadmap for any topic using AI and visualize it as an interactive graph.")

# Demo roadmap generator (works without external APIs)
def generate_demo_roadmap(topic: str):
    nodes = [
        {"id": "1", "label": f"{topic} Basics"},
        {"id": "2", "label": f"Core Concepts"},
        {"id": "3", "label": "Algorithms"},
        {"id": "4", "label": "Projects"},
        {"id": "5", "label": "Advanced Topics"},
    ]
    edges = [
        {"source": "1", "target": "2", "relation": "leads to"},
        {"source": "2", "target": "3", "relation": "enables"},
        {"source": "3", "target": "4", "relation": "applied in"},
        {"source": "4", "target": "5", "relation": "prepares for"},
    ]
    return {"nodes": nodes, "edges": edges}


# Generate roadmap (demo mode)
if st.sidebar.button("🚀 Generate Roadmap"):
    with st.spinner("Generating roadmap... Please wait ⌛"):
        roadmap_data = generate_demo_roadmap(topic)

        with open("roadmap_data.json", "w", encoding="utf-8") as f:
            json.dump(roadmap_data, f, indent=4)

        # Build PyVis graph
        g = Network(height="700px", width="100%", bgcolor="#f9f9f9", font_color="black", directed=True)

        if layout_type == "barnes_hut":
            try:
                g.barnes_hut()
            except Exception:
                g.repulsion()
        else:
            g.repulsion()

        for node in roadmap_data["nodes"]:
            g.add_node(
                node["id"],
                label=node.get("label", ""),
                title=node.get("label", ""),
                color=node_color,
                size=node_size,
                font={"size": font_size, "face": "arial", "color": "black"}
            )

        for edge in roadmap_data["edges"]:
            g.add_edge(
                edge.get("source"),
                edge.get("target"),
                title=edge.get("relation", ""),
                color=edge_color,
                width=2,
                arrows="to"
            )

        g.save_graph("roadmap.html")
        st.success("✅ Roadmap generated (demo mode)!")

        # Display graph
        st.subheader("📍 Interactive Roadmap")
        with open("roadmap.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=700, scrolling=True)

        # Download buttons
        st.subheader("🔧 Download Options")

        # Download JSON
        json_str = json.dumps(roadmap_data, indent=4)
        b64_json = base64.b64encode(json_str.encode()).decode()
        href_json = f'<a href="data:application/json;base64,{b64_json}" download="roadmap.json">Download JSON Roadmap 🔄</a>'
        st.markdown(href_json, unsafe_allow_html=True)

        # Download HTML
        with open("roadmap.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            b64_html = base64.b64encode(html_content.encode()).decode()
            href_html = f'<a href="data:text/html;base64,{b64_html}" download="roadmap.html">Download HTML File 📄</a>'
            st.markdown(href_html, unsafe_allow_html=True)

# ------------------ About Section ------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 About")
st.sidebar.markdown("""
**Developed by Aman Kumar**  
🎓 College Project Submission  
🚀 Helps users generate and visualize learning roadmaps  
""")
