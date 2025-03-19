# GPT LangChain Text To SQL Prompt Streamlit

使用 LangChain 串接 OpenAI 或 Ollama 並連接資料庫，讓 AI 瞭解資料庫結構、優化提示詞、實現 Text-to-SQL，並使用 Streamlit 建立互動式前端網頁。  


## Overview

- 模組：langchain-community v0.3.19，langchain-openai v0.3.7，langchain v0.3.20，langchain-ollama v0.2.3
- UI：streamlit v1.42.2

## Env

可以選擇 OpenAI 或 Ollama 作為 LLM，並設置所選擇 LLM 的環境變數。如果使用 OpenAI，則需要從 [OpenAI](https://platform.openai.com/) 獲取 API 金鑰（可能需要付費訂閱）。

```
# OPENAI 或 OLLAMA
LLM_TYPE='OLLAMA'

OPENAI_MODEL='gpt-4o-mini'
OPENAI_API_KEY=''

OLLAMA_URL='http://localhost:11434'
OLLAMA_MODEL='llama3.1:70b-instruct-q2_K'

DB_URL='postgresql://user:password@host:5432/database'
```

## Run

### Prerequisites

將你的提示語檔案放置在 `prompts` 目錄中。已經提供了一些範本。



### Install Module

```bash
pip install streamlit==1.42.2 pandas==2.2.3 python-dotenv==1.0.1 \
langchain-community==0.3.19 langchain-openai==0.3.7 langchain==0.3.20 \
langchain-ollama==0.2.3
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

- [LangChain 官方網站](https://python.langchain.com/)

