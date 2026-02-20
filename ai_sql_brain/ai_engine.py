import os
from openai import OpenAI
from schema_reader import load_schema
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCHEMA = load_schema()

SYSTEM_PROMPT = f"""
You are an Advanced SQLite AI Database Engineer.

DATABASE SCHEMA:
{SCHEMA}

VERY IMPORTANT SEARCH RULES:

1️⃣ Whenever user mentions any name, NEVER use '=' operator.

2️⃣ Always perform semantic-style fuzzy matching using:
LOWER(column_name) LIKE '%keyword%'.

3️⃣ For user identity search, ALWAYS check across:
- first_name
- middle_name
- last_name
- full_name (if exists)

Example:

User says: "details of robert"

You MUST generate:

WHERE LOWER(first_name) LIKE '%robert%'
OR LOWER(middle_name) LIKE '%robert%'
OR LOWER(last_name) LIKE '%robert%'
OR LOWER(full_name) LIKE '%robert%'

4️⃣ If multiple matches exist → return all.

5️⃣ Always generate ONLY SELECT queries.

6️⃣ Never access passwords or tokens.

7️⃣ Use JOIN when required.

Output ONLY SQL query.
"""

def generate_sql(question):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":question}
        ]
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql","").replace("```","")

    return sql
