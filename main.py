import streamlit as st
import time 
import os

from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Ollama Chatbot", page_icon="💬")

with st.sidebar:
    st.title('💬 Ollama Chatbot')
    
    # Select the model
    selected_model = st.selectbox('Choose a model', ['Mistral', 'Llama2', 'Code Llama'], key='selected_model')

    # Edit system prompt 
    system_prompt = st.text_area(
            label="System Prompt",
            value="You are a helpful assistant who answers questions in short sentences."
            )
    
    # Toggle to activate GPU 
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

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("How may I assist you today?")

# Set up the LLMChain, passing in memory
template = system_prompt + """

{history}
Human: {human_input}
AI: """

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm_chain = LLMChain(llm=Ollama(model=llm_model, num_gpu=activate_gpu), prompt=prompt, memory=memory)

# Display current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    if msg.type == "Human":
        with st.chat_message(msg.type, avatar="🧑‍💻"):
            st.write(msg.content)
    else:
       with st.chat_message(msg.type, avatar="💬"):
            st.write(msg.content) 

# Clear chat messages
def clear_chat_history():
    msgs.clear()
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# User input new prompt, generate, and display a new response
if prompt := st.chat_input():
    with st.chat_message("human", avatar="🧑‍💻"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="💬"):
        with st.spinner("Thinking..."):
            response = llm_chain.run(prompt)
        placeholder = st.empty()
        full_response = ''
        for item in response:
            full_response += item
            placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
        placeholder.markdown(full_response)