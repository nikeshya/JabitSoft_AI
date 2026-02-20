import re

def validate_sql(sql: str):

    if not sql:
        raise Exception("Empty SQL")

    sql_lower = sql.lower()

    # 🚨 ONLY SELECT ALLOWED
    if not sql_lower.strip().startswith("select"):
        raise Exception("Only SELECT queries allowed!")

    # 🔥 Forbidden keywords — exact match only
    forbidden = [
        "drop", "delete", "update",
        "insert", "alter", "truncate",
        "create", "replace"
    ]

    # Word boundary regex (prevents created_at issue)
    for f in forbidden:
        if re.search(rf"\b{f}\b", sql_lower):
            raise Exception(f"Unsafe SQL detected! Keyword: {f}")

    return True
