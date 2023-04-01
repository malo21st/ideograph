import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import random

def generate_edge_lst(size = 100):
    generator = np.random.default_rng()
    rnd = generator.normal(size=size)
    nodes = [int(abs(n) // 0.7) for n in rnd]
    node_dic, edge_lst = {0: [1]}, list()
    for node in nodes:
        if node_dic.get(node, False):
            if node_dic.get(node+1, False):
                node_dic[node+1].append(len(node_dic[node+1])+1)
            else:
                node_dic[node+1] = [1]
            edge_lst.append(((node, random.choice(node_dic[node])), (node+1, node_dic[node+1][-1])))
    return edge_lst

# layout
st.sidebar.header("AI Mind Map")
theme = st.sidebar.text_input("**お題を入力してください :**")

if theme:
    st.session_state['edge_lst'] = generate_edge_lst()
    st.session_state['nodes'] = [Node(id=str((0, 1)), label=theme, size=10)]
    st.session_state['edges'] = list()
    config = Config(width=750, height=750, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)

if st.sidebar.button("PUSH"):
    src, tgt = st.session_state['edge_lst'].pop(0)
    st.session_state['nodes'].append(Node(id=f"{tgt}", label=f"{tgt}", size=5))
    st.session_state['edges'].append(Edge(source=f"{src}", target=f"{tgt}"))
    config = Config(width=750, height=750, directed=False, physics=True, hierarchical=False)
    return_value = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
