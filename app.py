from config import DB_URL

import streamlit as st
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

from utils.llm_util import get_llm
from utils.rag_util import get_vector_store, run_rag
from utils.sql_util import clean_sql_response, convert_result_to_df


MAX_RETRIES = 3  # 最多重試次數

# 連接資料庫
db = SQLDatabase.from_uri(DB_URL)

# 取得資料庫資訊
table_info = db.get_table_info()

# 初始化 LLM 模型
llm = get_llm()

# 初始化 向量資料庫
vector_store = get_vector_store()

# Streamlit 頁面設定
st.set_page_config(page_title="SQL 查詢生成器", page_icon="💬", layout="wide")

# 頁面標題
st.title("SQL 查詢生成器 💬")


# 使用者輸入
user_input = st.chat_input("請輸入您的問題...")

if user_input:
    # 顯示使用者輸入
    with st.chat_message("user"):
        st.markdown(user_input)

    sql_query = None
    query_result = None
    memory = []

    # 嘗試 MAX_RETRIES 次
    for retry in range(1, MAX_RETRIES + 1):
        try:
            # 生成 SQL 查詢
            sql_query = run_rag(llm, vector_store, user_input, table_info, memory)

            # 清理 SQL 查詢字串
            sql_query = clean_sql_response(sql_query)

            # 直接用 LangChain 內建的 db.run() 執行 SQL 查詢
            query_result = db.run(sql_query, include_columns=True)

            # 如果執行成功，直接跳出 retry 迴圈
            break

        except Exception as e:
            # 將錯誤轉為字串
            error_message = str(e)

            # 記錄錯誤到 memory 中已供下次使用
            memory.append({
                "sql": sql_query,
                "error": error_message,
            })

            # 顯示在 Streamlit 上
            if retry < MAX_RETRIES:
                with st.chat_message("assistant"):
                    st.markdown(
                        f"❌ SQL 執行失敗：\n```sql\n{sql_query}\n```\n"
                        f"❗ 錯誤訊息：`{error_message}`，正在重新嘗試 ({retry}/{MAX_RETRIES})...")
            else:
                with st.chat_message("assistant"):
                    st.markdown(
                        f"❌ SQL 執行失敗：\n```sql\n{sql_query}\n```\n"
                        f"❗ 錯誤訊息：`{error_message}`")

                # 移除錯誤的 SQL 語法
                sql_query = None
                break

    # 順利產生 sql 後嘗試執行
    if sql_query:
        # 顯示在 Streamlit 上
        with st.chat_message("assistant"):
            st.markdown(f"**生成的 SQL 查詢：**\n```sql\n{sql_query}\n```")

        try:
            # 將查詢結果轉換成表格
            result_df = convert_result_to_df(query_result)

            # 顯示查詢結果
            if not result_df.empty:
                with st.chat_message("assistant"):
                    st.markdown(f"✅ 查詢成功，結果如下：")
                with st.chat_message("table"):
                    st.dataframe(result_df)
            else:
                # 沒有資料
                with st.chat_message("table"):
                    st.markdown(f"⚠️ 沒有查詢結果。")

        # 轉換錯誤
        except Exception as e:
            with st.chat_message("table"):
                st.markdown(f"❌ 結果處理錯誤：{e}")
