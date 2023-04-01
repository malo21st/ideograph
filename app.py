import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random

if 'count' not in st.session_state:
    st.session_state['count'] = 0
    st.session_state['nodes'] = [Node(id=0, label="0", size=10)]
    st.session_state['edges'] = list()
    config = Config(width=500, height=500, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)

if st.sidebar.button("PUSH"):
    st.session_state['count'] += 1
    tgt = st.session_state['count']
    src = random.choice(st.session_state['nodes'])
    st.session_state['nodes'].append(Node(id=tgt, label=f"{tgt}", size=5))
    st.session_state['edges'].append(Edge(source=src, target=tgt))
    config = Config(width=500, height=500, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
