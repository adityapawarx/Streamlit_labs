import streamlit as st
import openai

def run():
    st.title("📄 Lab 2")

    # Retrieve OpenAI API key
    openai_api_key = st.secrets["OPEN_API_KEY"]

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        # Set OpenAI API key (uncomment this if the key is needed)
        openai.api_key = openai_api_key

        # Sidebar: Language selection
        language = st.sidebar.selectbox(
            "Pick a language",
            options=["English", "German", "Japanese"],
            index=0  # Default language: English
        )

        # Sidebar: Summary type selection
        summary_type = st.sidebar.selectbox(
            "Pick a summary type",
            options=[
                "Summarize the document in 100 words",
                "Summarize the document in 2 connecting paragraphs",
                "Summarize the document in 5 bullet points",
            ]
        )

        # Sidebar: Checkbox for advanced model selection
        use_advanced_model = st.sidebar.checkbox("Use Advanced Model (GPT-4.0)")

        # File Uploader
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)",
            type=("txt", "md")
        )

        # Text Area for asking a question
        question = st.text_area(
            "Now ask a question about the document!", 
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file
        )

        # Check if file is uploaded and question is asked
        if uploaded_file and question:
            # Read and decode the uploaded document
            document = uploaded_file.read().decode()

            # Model selection based on checkbox
            model = "gpt-4" if use_advanced_model else "gpt-3.5-turbo"

            # Constructing the prompt with document, question, language, and summary type
            prompt = f"Here's a document: {document} \n\n---\n\n {question} \n\n"

            # Add language-specific instruction
            if language == "Japanese":
                prompt += "Respond in Japanese. \n\n"
            elif language == "German":
                prompt += "Answer in German. \n\n"
            elif language == "English":
                prompt += "Respond in English. \n\n"

            # Add summary type to the prompt
            prompt += f"Please summarize the document in the following format: {summary_type}."

            # Send to OpenAI API
            messages = [{"role": "user", "content": prompt}]
            
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )

                # Display the response
                st.write(response.choices[0].message['content'])
            
            except Exception as e:
                st.error(f"Error with OpenAI API: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    run()
