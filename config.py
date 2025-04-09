import os
from dotenv import load_dotenv



# 讀取 .env 變數
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# 資料庫連線
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise Exception("未在 .env 檔案中找到 DB_URL。")

# LLM 模型
LLM_TYPE = os.getenv("LLM_TYPE", "OPENAI")  # 默認為 OPENAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if LLM_TYPE == "OPENAI":
    if not OPENAI_API_KEY:
        raise Exception("未在 .env 檔案中找到 OPENAI_API_KEY。")
    if not OPENAI_MODEL:
        raise Exception("未在 .env 檔案中找到 OPENAI_MODEL")
elif LLM_TYPE == "OLLAMA":
    if not OLLAMA_URL:
        raise Exception("未在 .env 檔案中找到 OLLAMA_URL")
    if not OLLAMA_MODEL:
        raise Exception("未在 .env 檔案中找到 OLLAMA_MODEL")

# Embedding
OLLAMA_EMBEDDING_URL = os.getenv("OLLAMA_EMBEDDING_URL")
if not OLLAMA_EMBEDDING_URL:
    raise Exception("未在 .env 檔案中找到 OLLAMA_EMBEDDING_URL。")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")
if not OLLAMA_EMBEDDING_MODEL:
    raise Exception("未在 .env 檔案中找到 OLLAMA_EMBEDDING_MODEL。")
