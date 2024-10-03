import streamlit as st
import openai
import chromadb
from PyPDF2 import PdfReader
import os


def run():
    openai.api_key = st.secrets["OPEN_API_KEY"]
    def generate_embedding(text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response['data'][0]['embedding']
    def create_lab4_collection():
        client = chromadb.Client()
        collection = client.create_collection("Lab4Collection")
        pdf_folder = "./pdfs"
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
        for pdf_file in pdf_files:
            file_path = os.path.join(pdf_folder, pdf_file)
            text = extract_text_from_pdf(file_path)
            embedding = generate_embedding(text)
            collection.add(
                documents=[text],
                ids=[pdf_file],
                embeddings=[embedding]
            )
        return collection
    def extract_text_from_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    def search_vectorDB(query):
        query_embedding = generate_embedding(query)
        if "Lab4_vectorDB" not in st.session_state:
            st.error("Lab4 vector database has not been initialized.")
            return None
        collection = st.session_state.Lab4_vectorDB
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        documents = ""
        for i, doc in enumerate(results['documents'][0]):
            documents += f"Document {i+1}: {doc}\n"
        return documents
    def chatbot_response(query):
        relevant_documents = search_vectorDB(query)
        if relevant_documents is None or relevant_documents.strip() == "":
            use_rag = False
        else:
            use_rag = True
        conversation_history = [{"role": "system", "content": """
            You are a helpful assistant. After giving any response, always ask 'Do you want more info?'. 
            If the user says 'yes', provide additional details on the previous response. If the user says 'no', ask the user what else they would like help with. 
            If the user asks a new question, answer the new question and then ask 'Do you want more info?' again.
            Provide explanations in a way that a 10-year-old can understand.
        """}]
        if use_rag:
            conversation_history.append({
                "role": "system",
                "content": f"Relevant course information:\n{relevant_documents}"
            })
        conversation_history.extend(st.session_state.messages)
        conversation_history.append({"role": "user", "content": query})
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        assistant_response = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.title("Lab4: A Chatbot using RAG (retrieval-augmented generation)")
    if "Lab4_vectorDB" not in st.session_state:
        st.write("Initializing the vector database for the first time...")
        st.session_state.Lab4_vectorDB = create_lab4_collection()
        st.write("Vector database created and stored in session state!")
    prompt = st.chat_input("Ask anything")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        assistant_response = chatbot_response(prompt)
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

if __name__ == "__main__":
    run()