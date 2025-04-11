from config import OLLAMA_EMBEDDING_MODEL, OLLAMA_EMBEDDING_URL

import json
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from utils.prompt_util import get_sql_prompt


def get_vector_store():
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_EMBEDDING_URL)

    vector_store = InMemoryVectorStore(embeddings)

    # 取得 rags 資料夾下的 json 檔案
    loader = DirectoryLoader("./rags", glob="**/*.json", show_progress=True)

    for doc in loader.load():
        with open(doc.metadata["source"], "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):  # 確保 JSON 是列表
                for entry in data:
                    if "question" in entry and "response" in entry:
                        vector_store.add_documents(
                            [Document(
                                page_content=entry["question"],
                                metadata={"response": entry["response"]}
                            )]
                        )

    return vector_store


def run_rag(llm, vector_store, user_input, table_info, memory):
    """
    執行 RAG 流程，先檢索相似內容，再生成 SQL 查詢
    """
    
    # 進行向量檢索
    retrieved_docs = vector_store.similarity_search(user_input)

    # 準備 RAG 提供的 SQL 結果
    best_match = None
    if retrieved_docs:
        best_match = retrieved_docs[0]  # 取最相似的結果

    example = f"""
        問題:`{best_match.page_content}`
        回答: `{best_match.metadata["response"]}`
    """ if best_match else None

    # 整理記憶
    memory_str = ""
    if memory:
        for item in memory:
            memory_str += f"""
                SQL： {item['sql']}
                錯誤訊息：`{item['error']}`
            """


    prompt = get_sql_prompt(example, memory_str)

    # 產生 SQL 查詢
    messages = prompt.invoke({
        "input": user_input, 
        "table_info": table_info,
        "top_k": 20
    })
    
    response = llm.invoke(messages)
    return response.content