import streamlit as st
import openai

st.title("simple chat")

user_message = st.text_input(label="どうしましたか？")

if user_message:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=10,
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
    st.write(completion)
