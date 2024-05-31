import streamlit as st
import tempfile
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.readers.file.docs_reader import PDFReader




st.title("PDFへのQ&A")

index = st.session_state.get("index")

def on_chainge_file():
  if "index" in st.session_state:
    st.session_state.pop('index')

uploaded_file = st.file_uploader(
  label="Q&A対象のファイル", type="pdf", on_change=on_chainge_file
)

if uploaded_file and index is None:
  with st.spinner('準備中・・・'):
    with tempfile.NamedTemporaryFile() as f:
      f.write(uploaded_file.getbuffer())
      
      document = PDFReader().load_data(file=Path(f.name))
      
      llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
      service_context = ServiceContext.from_defaults(llm=llm)
      
      index = VectorStoreIndex.from_documents(
        documents=document, service_context=service_context
      )
      
      st.session_state["index"]  = index
      
      
if index is not None:
  question = st.text_input(label="質問")
  
  if question:
    with st.spinner(text="考え中・・・・"):
      query_engin = index.as_query_engine()
      answer = query_engin.query(question) # questionに近いベクトルの探索 => 回答
      st.write(answer.response)
      st.info(answer.source_nodes)
