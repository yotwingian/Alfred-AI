# 'chat_bot.py'
import os
import openai
import streamlit as st

# Check for API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    st.error("API key not found! Please set your OPENAI_API_KEY environment variable.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# Helper function to validate document length
def validate_document_length(content: str, max_length: int = 8000) -> str:
    if len(content) > max_length:
        return content[:max_length] + "..."
    return content

# Function to load document
def load_document(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return validate_document_length(content)
    except FileNotFoundError:
        st.error(f"Error: The file {file_path} was not found.")
        return "Document could not be loaded."

# Function to handle chatbot responses
def chatbot_response(user_input: str, document_content: str) -> str:
    try:
        # Build conversation history from session state
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful H&M assistant. Answer questions based on this document: "
                    + document_content
                    + ". Be concise and accurate. If you can't answer the question, refer to customer service."
                ),
            }
        ]
        
        # Add conversation history
        for message in st.session_state.history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
            
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error while processing your request: {e}")
        return "Sorry, I couldn't process your request."

# Main function
def main() -> None:
    st.title("Chatbot Alfred")

    # Initialize session state
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

    # Show the welcome message
    if not st.session_state.hello_message:
        response = "Hej jag heter Alfred och jag är HM's AI assistent, vad kan jag hjälpa dig med?"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.session_state.hello_message = True

    # User input
    prompt = st.chat_input("")
    if prompt:
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        # Get response from chatbot
        with st.chat_message("assistant"):
            response = chatbot_response(prompt, st.session_state.document)
            st.markdown(response)
        st.session_state.history.append({"role": "assistant", "content": response})

# Run the app
if __name__ == "__main__":
    main()
