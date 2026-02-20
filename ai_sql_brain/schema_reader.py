import sqlite3

def load_schema(db_path="ecommerce.db"):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_text = ""

    for t in tables:
        table = t[0]
        cursor.execute(f"PRAGMA table_info({table});")
        cols = cursor.fetchall()
        schema_text += f"\nTABLE: {table}\nCOLUMNS:\n"
        for c in cols:
            schema_text += f"{c[1]} ({c[2]})\n"

    conn.close()
    return schema_text
