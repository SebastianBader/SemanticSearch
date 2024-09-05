import streamlit as st

import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3


import chromadb

client = chromadb.PersistentClient(path="chromaDB")

st.set_page_config(initial_sidebar_state="collapsed")

st.sidebar.markdown("# Collection")
# collection_name = st.sidebar.selectbox('Choose Database', [c.name for c in client.list_collections()], 0, label_visibility='collapsed')

collection_name = "wikipedia_truncated"
collection = client.get_collection(name=collection_name) 
collection_info = ""

collection_info += f"### Information\n"
collection_info += f"- Name: '{collection_name}'\n"
collection_info += f"- Embedding dimension: {collection._model.dimension}\n"

if 'description' in collection.metadata:
    collection_info += f"### Description\n"
    collection_info += "_"+collection.metadata['description'] +"_\n"


collection_info += f"### System\n"
collection_info += f"- SQLite: '{sqlite3.sqlite_version}'\n"


st.sidebar.markdown(collection_info)
  
# f"""
# # Information:
# - Distance norm: '{collection._model.configuration_json['hnsw_configuration']['space']}'
# """)


st.header(f"_:blue[Fully Local Semantic Search]_")
st.subheader(f"Selected database: _'{collection_name}'_ with {collection.count()} documents")

question = st.text_input("Search question:", "Who is omnipotent?")

n_results = 5

results = collection.query(query_texts=[question], n_results=n_results, include=['metadatas', 'documents'])

if st.button("Ask a question"):
    st.divider()
    st.write(f"The current question is _'{question}'_. Below you will find the top {n_results} answer-documents.")


    tabs = st.tabs([results['metadatas'][0][i]['title'] for i in range(n_results)])

    for i in range(n_results):
        metadata = results['metadatas'][0][i]
        with tabs[i]:
            if 'title' in metadata:
                st.header(metadata['title'])
            if 'url' in metadata:
                st.page_link(metadata['url'], icon="🔗", label=f"{metadata['url']}")
            st.markdown('<i>'+results['documents'][0][i].split('\n')[0]+'…</i>', unsafe_allow_html=True)
 