import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import openai
import numpy as np
import random
from tenacity import retry, wait_fixed, stop_after_attempt
import json

openai.api_key = st.secrets['api_key']

def tuple2key(tpl):
    return f"{tpl[0]}_{tpl[1]}"

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

def initialize():
    st.session_state['edge_lst'] = generate_edge_lst()
    st.session_state['node'] = list()
    st.session_state['edge'] = list()
    st.session_state['label'] = dict()

if 'theme' not in st.session_state:
    st.session_state['theme'] = ""
    

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_AI_word(word, NG_word):
    question = f"""ＮＧワード を避けて、{word} に関連のある単語を１つ答えなさい
# ＮＧワード: {NG_word}

# 単語: 
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        temperature=random.random()
    )
    AI_word = response.choices[0]['message']['content'].strip()
    if len(AI_word) > 25:
        AI_word = AI_word[:10]
        get_AI_word(word, NG_word)
    return AI_word

# layout
st.sidebar.header("AI Mind Map")
theme = st.sidebar.text_input("**お題を入力してください :**")

if theme != st.session_state['theme']:
    initialize()
    st.session_state['node'].append(Node(id=tuple2key((0, 1)), label=theme, size=10))
    st.session_state['label'][tuple2key((0, 1))] = theme
    st.session_state['theme'] = theme

if st.sidebar.button("think... THINK !"):
    src, tgt = st.session_state['edge_lst'].pop(0)
    word = st.session_state['label'][tuple2key(src)]
    AI_word = get_AI_word(word, list(st.session_state['label'].values()))
    st.session_state['node'].append(Node(id=tuple2key(tgt), label=AI_word, size=5))
    st.session_state['edge'].append(Edge(source=tuple2key(src), target=tuple2key(tgt), width=3))
    st.session_state['label'][tuple2key(tgt)] = AI_word
#     st.sidebar.write(f"発想した数：{len(st.session_state['node']) - 1}")
#     st.sidebar.write(f"{src} {tgt} {word} {AI_word}")
#     st.sidebar.write(f"{st.session_state['label'].values()}")
#     st.sidebar.write(f"{st.session_state['edge_lst'][:3]}")

if st.session_state['theme']:
    mmap_dic = dict()
    label_dic = st.session_state['label']
    mmap_dic["nodes"] = [{"id": node.id, "label": label_dic[node.id]} for node in st.session_state['node']]
    mmap_dic["edges"] = [{"id": idx, "source": edge.source, "target": edge.to} for idx, edge in enumerate(st.session_state['edge'])]
    st.sidebar.download_button(
        label="JSONダウンロード",
        data=json.dumps(mmap_dic),
        file_name='mind_map.json',
        mime='text',
    )

if st.session_state['theme']:
    config = Config(width=800, height=800, directed=False, physics=True, hierarchical=False)
    result = agraph(nodes=st.session_state['node'], edges=st.session_state['edge'], config=config)
