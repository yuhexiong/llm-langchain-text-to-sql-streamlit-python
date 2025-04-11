# LLM LangChain Text To SQL Streamlit

**(also provided Traditional Chinese version document [README-CH.md](README-CH.md).)**


Use LangChain to integrate with OpenAI or Ollama and connect to a database, enabling the AI to understand the database structure, enhance prompts with Retrieval-Augmented Generation (RAG), achieve Text-to-SQL, and build an interactive frontend web page with Streamlit.  

## Overview
- Module: langchain-community v0.3.19, langchain-openai v0.3.7, langchain v0.3.20, langchain-ollama v0.2.3
- UI: streamlit v1.42.2

## Env

Able to choose OpenAI or Ollama as the LLM and set the environment variables for the selected LLM. If using OpenAI, an API key must be obtained from [OpenAI](https://platform.openai.com/) (a paid subscription may be required). Additionally, the embedding model used for RAG can be different from the selected LLM.  

```
# LLM OPENAI or OLLAMA
LLM_TYPE='OLLAMA'

OPENAI_MODEL='gpt-4o-mini'
OPENAI_API_KEY=''

OLLAMA_URL='http://localhost:11434'
OLLAMA_MODEL='gemma3:27b'

# Embedding
OLLAMA_EMBEDDING_URL='http://localhost:11434'
OLLAMA_EMBEDDING_MODEL='llama3.1:70b-instruct-q2_K'

# Database
DB_URL='postgresql://user:password@host:5432/database'
```

## Run

### Prerequisites

Modify the prompt in the code based on your database information. Some templates have already been provided.  

### Install Module

```bash
pip install -r requirements.txt
```


### Run

#### Script Version
```bash
python script.py
```

#### Web Version
```bash
streamlit run app.py
```

server running at `http://localhost:8501`


## UI

![UI Home](./images/ui-home.png)

![UI Result](./images/ui-result.png)

## References

- [LangChain Official Website](https://python.langchain.com/)