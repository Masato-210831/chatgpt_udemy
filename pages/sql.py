import streamlit as st

st.title("Text-to-SQL")

question = st.text_input(label="質問")

if question:
  sql = "select count(*) from product"
  answer = "商品は100件です。"
  st.info(sql)
  st.success(answer)