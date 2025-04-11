import re

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from langchain.chains import create_sql_query_chain
from langchain.schema import HumanMessage
from langchain_community.utilities import SQLDatabase

from config import DB_URL
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
result_df = None

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


# 順利產生 result_df 後嘗試執行
if user_input and result_df is not None and not result_df.empty:

    # 讓 LLM 生成 Matplotlib 程式碼
    plot_prompt = f"""
    請根據 使用者問題 '{user_input}' 以及 Pandas DataFrame `result_df` 繪製 Matplotlib 圖表：
    {result_df.head().to_string()}
    
    並確保符合以下要求：

    1. **請嚴格遵守：**  
    - **只能使用 `pd` 和 `matplotlib` 和 `plt` 套件，且不需要寫任何 import ，不允許操作其他套件。
    - **禁止** 重新定義 `result_df`，不要包含 `result_df = ...` 或 `pd.DataFrame({...})`。  
    - **請直接使用** `result_df`，假設它已經存在且包含完整數據，不需要創建新數據。  
    - **不得修改 `result_df` 的數據**，只能轉換格式（如 `pd.to_datetime()`）。

    2. **程式碼格式：**  
    - **請使用 `fig, ax = plt.subplots()`** 來建立圖表。  
    - **請使用 `ax.plot()`，而不是 `plt.plot()`。**  
    - **請確保有產生 `fig` 變數，但不需要返回 `fig` 變數，不要使用 `plt.show()`**。  

    3. **圖表設定：**  
    - 設定適當的 `figsize`，長度設定為 8。  
    - 使用 `ax.grid(True)` 啟用網格線。  
    - 設定合適的標題與標籤，請確保 `plt` 參數有設定中文字型，才能顯示中文，使用 `plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']` 。  
    - **只有在資料包含時間序列時才可使用折線圖**。例如，顯示時間變化的數據，如每日銷售、溫度隨時間變化等，才能使用折線圖。
    - **如果資料中沒有時間變數，請避免使用折線圖**，而應選擇其他適合的圖表類型，例如條形圖、圓餅圖等。
    - 請確保根據資料的性質選擇正確的圖表。折線圖僅用於顯示時間序列數據，其他情境請選擇其他圖表形式。
    - **如果 X 軸的標籤過多，請調整顯示方式**，例如將 X 軸標籤旋轉為斜體（例如 45 度角），以避免文字擠在一起。若標籤仍然過於擠密，考慮將標籤改為垂直顯示，或僅顯示部分標籤（例如每隔一個顯示一個標籤），以提高可讀性。

    **請只有 Python 程式碼，**不要包含任何說明或解釋！**  
    **請確保程式碼沒有 `result_df = ...`，否則無效！**
    **請確保程式碼沒有 return 任何東西！**
    """

    # 取得 LLM 生成的 Python 程式碼
    generated_code = llm([HumanMessage(content=plot_prompt)]).content

    # 使用正則表達式移除 Markdown 程式碼
    clean_code = re.sub(r"```(python)?\n", "", generated_code).strip()
    clean_code = re.sub(r"\n```", "", clean_code)

    plot_module = {"matplotlib": matplotlib, 'plt': plt, "pd": pd, "result_df": result_df}
    # 執行生成的程式碼
    exec(clean_code, plot_module)

    # 從 `plot_module` 取出 `fig`
    fig = plot_module.get("fig")

    # 顯示圖表到 Streamlit
    st.pyplot(fig=fig, use_container_width=False)
