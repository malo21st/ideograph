import streamlit
from streamlit_agraph import agraph, Node, Edge, Config
import time

nodes ,edges = [], []
config = Config(width=750, height=950, directed=False, physics=True, hierarchical=False)
nodes.append(Node(id=0, label="0", size=25))
for i in range(1, 5):
    nodes.append(Node(id=i, label=f"{i}", size=25))
    edges.append(Edge(source=0, target=i))
    agraph(nodes=nodes, edges=edges, config=config)
    st.write(i)
    time.sleep(3)
# return_value = agraph(nodes=nodes, edges=edges, config=config)
