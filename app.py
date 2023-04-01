import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import time

if 'count' not in st.session_state:
    st.session_state['count'] = 0
    st.session_state['nodes'] = [Node(id=0, label="0", size=10)]
    st.session_state['edges'] = list()
    config = Config(width=500, height=500, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
# if 'nodes' not in st.session_state:
#     st.session_state['nodes'] = list()
    
# if 'edges' not in st.session_state:
    
if st.sidebar.button("PUSH"):
# if st.session_state['count'] < 6:
# for i in range(1, 6):
    st.session_state['count'] += 1
    i = st.session_state['count']
    st.session_state['nodes'].append(Node(id=i, label=f"{i}", size=5))
    st.session_state['edges'].append(Edge(source=0, target=i))
    config = Config(width=500, height=500, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
#     time.sleep(2)
    
# agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
# return_value = agraph(nodes=nodes, edges=edges, config=config)
