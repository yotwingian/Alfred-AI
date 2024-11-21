import os
import openai
import streamlit as st

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def load_document(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

def chatbot_response(user_input: str, document_content: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You only answer questions related to this document: " + 
                 document_content +
                 ". If you can't answer the question, refer to cumstomer service"},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."


def main() -> None:

    st.title("Chatbot Alfred")

    # Initialize session state to store conversation
    if "history" not in st.session_state:
        st.session_state.history = []

    if "document" not in st.session_state:
        st.session_state.document = load_document("faq_hm.txt")
    
    if "hello_message" not in st.session_state:
        st.session_state.hello_message = False
    
    
    # Display chat messages from history
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.hello_message:
        response = "Hej jag heter Alfred och jag är HM's Ai assistent, vad kan jag hjälpa dig med?"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.session_state.hello_message = True
    
    prompt = st.chat_input("")
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = chatbot_response(prompt, st.session_state.document)
            st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})
            
    

if __name__ == '__main__':
    main()