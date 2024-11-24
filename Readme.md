# Chatbot Alfred
(POC, School project, LIA)

Chatbot Alfred is an AI assistant designed to answer questions based on an txt document using OpenAI's GPT-API. The bot is built using Python and Streamlit. In this example we are using HM's FAQ as the context document.

### Features

- Loads a document to use as a context, in this case HM's FAQ 
- Conversation history.
- Error handling.

### Prerequisites

- Python 3.7+
- Streamlit and OpenAI Libs
- OpenAI API key

### Install required packages

    ```bash
    pip install -r requirements.txt
    ```


### Set up OpenAI API key

    Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY=your-openai-api-key
    ```

### Prepare your document
    Ensure you have a text file named `faq_hm.txt` with your FAQ content in the same directory as `chat_bot.py`.


### Customization
- You also change to another LLM instead of open AI gpt.
-  The function `validate_document_length` can be adjusted to change the maximum content length.
-  Modify the `system_message` in the `chatbot_response` function to customize the assistant's role and behavior.
