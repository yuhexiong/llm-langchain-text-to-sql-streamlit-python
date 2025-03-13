# GPT LangChain Text To SQL Prompt Streamlit

使用 LangChain 串接 OpenAI 並連接資料庫，讓 AI 瞭解資料庫結構、優化提示詞、實現 Text-to-SQL，並使用 Streamlit 建立互動式前端網頁。  


## Overview

- 模組: langchain-community v0.3.19、langchain-openai v0.3.7、langchain v0.3.20
- UI: streamlit v1.42.2


## Run

### Prerequisites


1. 從 ****[OpenAI](https://platform.openai.com/)**** 取得 API 金鑰（可能需要付費訂閱），並將金鑰更新到你的 **`.env`** 檔案。
2. 將你的提示詞（prompt）筆記放在 **`prompts`** 資料夾中。範例檔案已提供。


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

