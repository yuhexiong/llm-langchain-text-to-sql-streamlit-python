from config import LLM_TYPE, OLLAMA_MODEL, OLLAMA_URL, OPENAI_API_KEY, OPENAI_MODEL

from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI



def get_llm():
    # 初始化 LLM 模型
    if LLM_TYPE == "OPENAI":
        return ChatOpenAI(model=OPENAI_MODEL, temperature=0, api_key=OPENAI_API_KEY)
    elif LLM_TYPE == "OLLAMA":
        return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL)

    else:
        raise Exception(f"未支援的 LLM_TYPE: {LLM_TYPE}")

