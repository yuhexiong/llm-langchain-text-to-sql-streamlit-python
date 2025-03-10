import re
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
import ast
from langchain.prompts import PromptTemplate

# 讀取 .env 變數
load_dotenv()

# 取得 OpenAI API 金鑰
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("未在 .env 檔案中找到 OPENAI_API_KEY。")

# 取得資料庫連線字串
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise Exception("未在 .env 檔案中找到 DB_URL")

# 連接資料庫
db = SQLDatabase.from_uri(DB_URL)

# 取得 `table_info`
table_info = db.get_table_info()

# 初始化 OpenAI 模型
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

# 讀取 `./prompts/` 內所有 `.txt` 檔案
def load_context_from_folder(folder_path="./prompts"):
    context = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                context += file.read() + "\n\n"
    return context.strip()

# 讀取 Context
context_text = load_context_from_folder()

# 自訂 Prompt，包含 `context_text`
prompt = PromptTemplate.from_template(
    f"""
    {context_text}

    你是一個 SQL 生成器，請基於以下的 `table_info` 資訊生成一個 SQL 查詢：

    - `table_info`: {{table_info}}
    - 使用者的問題: {{input}}
    - 每次獲取資料數量: {{top_k}}

    請輸出完整的 SQL 查詢，不要包含任何解釋文字。
    """
)

# 創建 SQL 查詢鏈
chain = create_sql_query_chain(llm, db, prompt=prompt)

# 處理 SQL 查詢字串
def clean_sql_response(sql_query):
    """
    處理 LangChain 回傳的 SQL 查詢字串，移除前綴與雜訊。
    """
    # 1. 移除前綴 "SQLQuery: "
    sql_query = re.sub(r"^SQLQuery:\s*", "", sql_query).strip()

    # 2. 處理 Markdown 格式 ```sql ... ```
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query

# 使用者輸入問題
user_input = input("請輸入您的問題：")

if user_input:
    try:
        sql_query = chain.invoke({
            "question": user_input,
            "table_info": table_info,
            "top_k": 20
        })

        sql_query = clean_sql_response(sql_query)
        print(f"\n生成的 SQL 查詢：\n{sql_query}\n")

        query_result = db.run(sql_query, include_columns=True)

        query_result = re.sub(r"Decimal\('([\d\.]+)'\)", r'\1', query_result)

        parsed_result = ast.literal_eval(query_result)

        if isinstance(parsed_result, list) and parsed_result:
            result_df = pd.DataFrame(parsed_result)
        else:
            result_df = pd.DataFrame()

        if not result_df.empty:
            print("\n✅ 查詢成功，結果如下：")
            print(result_df)
        else:
            print("\n⚠️ 沒有查詢結果。")

    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
