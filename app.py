import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import openai
import numpy as np
import random

openai.api_key = st.secrets['api_key']

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

def get_AI_word(word):
    question = f"{word} に関連のある単語を１つ答えて下さい"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        temperature=random.random()
    )
    AI_word = response.choices[0]['message']['content'].strip()
    if AI_word in st.session_state['label'].values():
        get_AI_word(word)
    return AI_word

if 'edge_lst' not in st.session_state:
    st.session_state['first_time'] = True
    st.session_state['edge_lst'] = generate_edge_lst()
    st.session_state['nodes'] = list()
    st.session_state['edges'] = list()
    st.session_state['label'] = dict()

# layout
st.sidebar.header("AI Mind Map")
theme = st.sidebar.text_input("**お題を入力してください :**")

if theme and st.session_state['first_time']:
    st.session_state['nodes'].append(Node(id=str((0, 1)), label=theme, size=10))
    st.session_state['label'][str((0, 1))] = theme
    config = Config(width=750, height=750, directed=False, physics=True, hierarchical=False)
    result = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
    st.session_state['first_time'] = False
    st.sidebar.write(f"Node: {len(st.session_state['nodes'])}")

if st.sidebar.button("PUSH"):
    src, tgt = st.session_state['edge_lst'].pop(0)
    word = st.session_state['label'][f"{src}"]
    AI_word = get_AI_word(word)
    st.session_state['nodes'].append(Node(id=f"{tgt}", label=AI_word, size=5))
    st.session_state['edges'].append(Edge(source=f"{src}", target=f"{tgt}"))
    config = Config(width=750, height=750, directed=False, physics=True, hierarchical=False)
    result = agraph(nodes=st.session_state['nodes'], edges=st.session_state['edges'], config=config)
    st.session_state['label'][f"{tgt}"] = AI_word
    st.sidebar.write(f"{src} {tgt} {word} {AI_word}")
    st.sidebar.write(f"{st.session_state['label'].values()}")
