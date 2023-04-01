import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import time

if 'count' not in st.session_state:
    st.session_state['count'] = 0
    
if 'nodes' not in st.session_state:
    st.session_state['nodes'] = list()
    
if 'edges' not in st.session_state:
    st.session_state['edges'] = list()
    
config = Config(width=750, height=950, directed=False, physics=True, hierarchical=False)
nodes.append(Node(id=0, label="0", size=25))

if st.button("PUSH"):
    st.session_state['count'] += 1
    i = st.session_state['count']
    st.write(i)
    st.session_state['nodes'].append(Node(id=i, label=f"{i}", size=25))
    st.session_state['edges'].append(Edge(source=0, target=i))
    agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
    time.sleep(3)
# return_value = agraph(nodes=nodes, edges=edges, config=config)
