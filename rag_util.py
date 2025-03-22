import ast
import json
import os
import re

from langchain_ollama import OllamaEmbeddings
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
from langchain_community.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from prompt_util import get_prompt


# 讀取 .env 變數
load_dotenv()

def get_vector_store():
    # embedding
    OLLAMA_EMBEDDING_URL = os.getenv("OLLAMA_EMBEDDING_URL")
    if not OLLAMA_EMBEDDING_URL:
        raise Exception("未在 .env 檔案中找到 OLLAMA_EMBEDDING_URL。")
    OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL")
    if not OLLAMA_EMBEDDING_MODEL:
        raise Exception("未在 .env 檔案中找到 OLLAMA_EMBEDDING_MODEL。")

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


def run_rag(llm, vector_store, user_input, table_info):
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

    prompt = get_prompt(example)

    # 產生 SQL 查詢
    messages = prompt.invoke({
        "input": user_input, 
        "table_info": table_info,
        "example": example,
        "top_k": 20
    })
    
    response = llm.invoke(messages)
    return response.content