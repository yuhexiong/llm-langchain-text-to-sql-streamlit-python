import os

from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI


# 讀取 .env 變數
load_dotenv()

def get_llm():
    # 初始化 LLM 模型
    LLM_TYPE = os.getenv("LLM_TYPE", "OPENAI")  # 默認為 OPENAI

    if LLM_TYPE == "OPENAI":
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        OPENAI_MODEL = os.getenv("OPENAI_MODEL")

        if not OPENAI_API_KEY:
            raise Exception("未在 .env 檔案中找到 OPENAI_API_KEY。")
        if not OPENAI_MODEL:
            raise Exception("未在 .env 檔案中找到 OPENAI_MODEL")

        return ChatOpenAI(model=OPENAI_MODEL, temperature=0, api_key=OPENAI_API_KEY)

    elif LLM_TYPE == "OLLAMA":
        OLLAMA_URL = os.getenv("OLLAMA_URL")
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

        if not OLLAMA_URL:
            raise Exception("未在 .env 檔案中找到 OLLAMA_URL")
        if not OLLAMA_MODEL:
            raise Exception("未在 .env 檔案中找到 OLLAMA_MODEL")

        return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL)

    else:
        raise Exception(f"未支援的 LLM_TYPE: {LLM_TYPE}")

