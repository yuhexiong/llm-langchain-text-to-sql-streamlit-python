import re
import ast
import pandas as pd



def clean_sql_response(sql_query: str) -> str:
    """
    處理 LangChain 回傳的 SQL 查詢字串，移除前綴與雜訊。
    """
    # 1. 移除前綴 "SQLQuery: "
    sql_query = re.sub(r"^SQLQuery:\s*", "", sql_query).strip()

    # 2. 處理 Markdown 格式 ```sql ... ```
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query



def convert_result_to_df(query_result: None | str) -> pd.DataFrame:
    """
    轉換 LangChain 回傳的 SQL 查詢結果為 pandas DataFrame。
    """

    if query_result == None or query_result == "":
        return pd.DataFrame()

    # 把 Decimal 轉成數字
    query_result = re.sub(r"Decimal\('([\d\.]+)'\)", r'\1', query_result)

    # 把 Date 轉成字串
    query_result = re.sub(
        r"datetime\.date\((\d{4}), (\d{1,2}), (\d{1,2})\)", r'"\1-\2-\3"', query_result)

    # 把 DataTime 轉成字串
    query_result = re.sub(
        r"datetime\.datetime\((\d{4}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), tzinfo=datetime.timezone.utc\)", 
        r'"\1-\2-\3 \4:\5:\6"', query_result)

    query_result = re.sub(
        r"datetime\.datetime\((\d{4}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), tzinfo=datetime.timezone.utc\)", 
        r'"\1-\2-\3 \4:\5:00"', query_result)

    # 將字串轉換成 Object list
    parsed_result = ast.literal_eval(query_result)

    # 轉換結果為 DataFrame
    if not isinstance(parsed_result, list) and parsed_result:
        return pd.DataFrame()

    return pd.DataFrame(parsed_result)