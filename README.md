
# Ollama Streamlit

Run large language models locally using Ollama, Langchain, and Streamlit.

We use Mistral 7b model as default model. You can change other supported models, see the [Ollama model library](https://github.com/jmorganca/ollama#model-library).

## Setup

Install Ollama

[Download Ollama](https://ollama.ai/download)

Download Mistral 7b
```bash
ollama pull mistral
```

Clone this project

```bash
  git clone https://github.com/agnanp/Ollama-Streamlit.git
```

Go to the project directory

```bash
  cd Ollama-Streamlit
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the streamlit

```bash
  streamlit run main.py
```


## References

 - [Llama 2 Chat](https://github.com/dataprofessor/llama2/tree/master)
 - [ai-chatbot-ollama](https://github.com/lalanikarim/ai-chatbot-ollama)
 - [Streamlit chat message history](https://python.langchain.com/docs/integrations/memory/streamlit_chat_message_history)

