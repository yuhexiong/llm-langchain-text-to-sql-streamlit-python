import os

from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

from utils.llm_util import get_llm
from utils.prompt_util import get_prompt
from utils.sql_util import clean_sql_response, convert_result_to_df

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


# 初始化 LLM 模型
llm = get_llm()

# 自訂 Prompt
prompt = get_prompt()

# 創建 SQL 查詢鏈
chain = create_sql_query_chain(llm, db, prompt=prompt)


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

        # 將查詢結果轉換成表格
        result_df = convert_result_to_df(query_result)

        if not result_df.empty:
            print("\n✅ 查詢成功，結果如下：")
            print(result_df)
        else:
            print("\n⚠️ 沒有查詢結果。")

    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
