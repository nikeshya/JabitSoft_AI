import sqlite3
from ai_engine import generate_sql
from sql_guard import validate_sql

class Brain:

    def __init__(self, db_path="ecommerce.db"):
        self.db_path = db_path

    def execute(self, question):

        print("\n🧠 Thinking...")

        sql = generate_sql(question)

        print("\nGenerated SQL:\n", sql)

        validate_sql(sql)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()

            conn.close()

            if not rows:
                return "No results found."

            return rows

        except Exception as e:
            return f"Execution Error: {str(e)}"
