import streamlit as st
import time 
import os

from langchain.llms import Ollama


st.set_page_config(page_title="💬 Ollama Chatbot")

with st.sidebar:
    st.title('💬 Ollama Chatbot')
    
    selected_model = st.selectbox('Choose a model', ['Mistral', 'Llama2', 'Code Llama'], key='selected_model')

    system_prompt = st.text_area(
            label="System Prompt",
            value="You are a helpful assistant who answers questions in short sentences."
            )
    gpu_on = st.toggle('Activate GPU')
# Select the model 
if selected_model == "Mistral":
    llm_model = "mistral"
elif selected_model == "Llama2":
    llm_model = "llama2"
else:
    llm_model = "codellama"

# Activate the GPU
if gpu_on:
    activate_gpu = 1
else:
    activate_gpu = 0

llm = Ollama(
    model=llm_model, num_gpu=activate_gpu
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
def generate_llm_response(prompt_input):
    string_dialogue = f"{system_prompt}. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    try:
        output = llm.__call__(prompt=f"{string_dialogue} {prompt_input} Assistant: ") 
    except Exception:
        with st.status("Downloading data..."):
            st.write("pulling manifest")
            os.system(f"ollama pull {llm_model}")
            st.write("download complete!")
            time.sleep(0.1)
            st.rerun()

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
            response = generate_llm_response(prompt)
            placeholder = st.empty()
            full_response = ''
        for item in response:
            full_response += item
            placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
        placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)