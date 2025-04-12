from langchain.prompts import PromptTemplate
import pandas as pd


def get_sql_prompt(example: str | None, memory: str | None):
    """
    自訂產生 SQL 的 Prompt
    """

    prompt_template = f"""
        你是一個 SQL 生成器，請基於以下資訊生成一個 SQL 查詢：
        
        - 資料表格式: {{table_info}}
        - 使用者的問題: {{input}}
        - 每次獲取資料數量: {{top_k}}

        請輸出完整的 SQL 查詢，不要包含任何解釋文字，並符合下面規則。

        ### 1. SQL 語法規則  

        - **表格名稱必須加上雙引號**  
        - **欄位名稱不可使用任何符號**  
        - 範例：`SELECT 名稱 FROM "table_name"`  

        - **聚合函數必須加括號**  
        - 範例：`SELECT MIN(日期) FROM "table_name"`  

        ### 2. `GROUP BY` 使用規則  

        - **當問題涉及「最高」「最低」「平均」「總和」時，一定要 `GROUP BY`**  
        - **當問題要求「每個對象」、「每個類別」、「每個項目」時，一定要 `GROUP BY`**  
        - 範例：`SELECT 類別, AVG(數值) FROM "table_name" GROUP BY 類別`  

        - **選擇正確的 `GROUP BY` 屬性**  
        - 若問題涉及某項目（如：「哪個項目的值最高？」）➡ `GROUP BY 項目名稱`  
        - 若問題涉及某類別（如：「哪個類別的平均值最高？」）➡ `GROUP BY 類別名稱`  
        - 若問題未明確說明，預設使用 `GROUP BY 項目名稱`  
        - **`SELECT` 中必須包含 `GROUP BY` 的欄位**  
        - 範例：`SELECT 類別, MAX(數值) FROM "table_name" GROUP BY 類別`  

        """

    if example is not None and example != "":
        prompt_template += f"""

        以下是檢索出最相關的範例問答：
            {example}
        """

    if memory is not None and memory != "":
        prompt_template += f"""

        以下是目前為止的嘗試及錯誤訊息：
            {memory}
        """

    return PromptTemplate.from_template(prompt_template)



def get_plot_prompt(user_input: str, result_df: pd.DataFrame) -> str:
    """
    自訂產生 Matplotlib 程式碼的 Prompt
    """

    return f"""
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