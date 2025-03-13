# GPT LangChain Text To SQL Prompt Streamlit

**(also provided Traditional Chinese version document [README-CH.md](README-CH.md).)**


Use LangChain to integrate with OpenAI and connect to the database, enabling the AI to understand the database structure, optimize prompts, achieve Text-to-SQL, and build an interactive frontend web page with Streamlit.

## Overview
- Module: langchain-community v0.3.19, langchain-openai v0.3.7, langchain v0.3.20
- UI: streamlit v1.42.2

## Run

### Prerequisites

1. Obtain an API key from [OpenAI](https://platform.openai.com/) (a paid subscription may be required) and update your `.env` file with the key.
2. Place your prompt notes in the `prompts` directory. Some samples are already provided.

### Install Module

```bash
pip install streamlit==1.42.2 pandas==2.2.3 python-dotenv==1.0.1 \
langchain-community==0.3.19 langchain-openai==0.3.7 langchain==0.3.20
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
