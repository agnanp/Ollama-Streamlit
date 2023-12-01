import streamlit as st
import time 

from langchain.llms import Ollama

st.set_page_config(page_title="Mistral Chatbot")

llm = Ollama(
    model="mistral", num_gpu=1
)

with st.sidebar:
    st.title('💬 Mistral Chatbot')

    system_prompt = st.text_area(
            label="System Prompt",
            value="You are a helpful assistant who answers questions in short sentences."
            )
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar="🧑‍💻"):
            st.write(message["content"])
    else:
       with st.chat_message(message["role"], avatar="💬"):
            st.write(message["content"]) 

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = f"{system_prompt}. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = llm.__call__(prompt=f"{string_dialogue} {prompt_input} Assistant: ") 
    return output

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar="💬"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
        for item in response:
            full_response += item
            placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
        placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)