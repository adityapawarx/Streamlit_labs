import streamlit as st
import openai
import requests
import numpy as np


def run():
    #TITLE
    st.title("A Chatbot made using Streamlit and OpenAI")


    #KEYS
    openai_api_key = st.secrets["OPEN_API_KEY"]
    openai.api_key = openai_api_key


    #CHAT BOT
    #Initialize session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #The initial message our AI wwill be displaying
    if not st.session_state.messages:    
        st.session_state.messages.append({"role": "system", "content": "Hi, I am Jarvis. How can I help you today?."})

    #Dis play all messages using "for m in ms" kinda code
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    #Chat Input from a user
    prompt = st.chat_input("Ask me anything!")
    if prompt:
        
        #Displaying user's prompt in the UI
        with st.chat_message("user"):
            st.markdown(prompt)
        
        #Adding user's prompt to the session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        #Add a conversation buffer of n=2
        conversation_buffer = []

        user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"]

        #We are going to retain the last 2 messages of both
        if len(user_messages) > 2:
            last_2_user_messages = user_messages[-2:]
            corresponding_assistant_messages = assistant_messages[-2:] if len(assistant_messages) >= 2 else assistant_messages

            # Build the buffer with interleaved user and assistant messages
            conversation_buffer = [msg for pair in zip(last_2_user_messages, corresponding_assistant_messages) for msg in pair]
        else:
            conversation_buffer = st.session_state.messages        

        #API call is here 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        bots_reply = response.choices[0].message["content"]

        st.session_state.messages.append({"role": "assistant", "content": bots_reply})

        #Displaying bot's reply
        with st.chat_message(bots_reply):
            st.markdown(bots_reply)
 
    
if __name__ == "__main__":
    run()   
    
    
