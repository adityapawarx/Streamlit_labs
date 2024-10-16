import streamlit as st
import openai


def run():
    st.title("📄 Lab 1")

    st.write("Paste your token below and upload a document below and ask a question about it – GPT will answer!")

    openai_api_key = st.text_input("OpenAI API Key", type="password")

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        openai.api_key = openai_api_key

        uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

        question = st.text_area("Now ask a question about the document!", placeholder="Can you give me a short summary?", disabled=not uploaded_file)

        if uploaded_file and question:
            document = uploaded_file.read().decode()
            messages = [
                {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            st.write(response.choices[0].message['content'])

