import json
import requests
import os
from datetime import datetime
from tqdm import tqdm

# ---------------- CONFIG ----------------

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen3:8b"

DATA_PATH = "clean_chat_history.json"
OUTPUT_JSON = "quality_reports_qwen3.json121"

BATCH_SIZE = 500


# ---------------- UTIL ----------------

def extract_json(text):
    if not text:
        raise ValueError("Empty response from model")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Invalid JSON format")

    return json.loads(text[start:end + 1])


def call_model(session_history):
    prompt = f"""
You are an AI quality analyst.

Analyze the chatbot conversation below and RETURN ONLY VALID JSON.

IMPORTANT RULES:
- "summary" MUST NOT be empty
- "summary" must clearly explain:
  1. What the user problem was
  2. What the assistant did
  3. Whether the problem was resolved

Return JSON strictly in this format:

{{
  "user_satisfaction": "high|medium|low",
  "bot_accuracy": "high|medium|low",
  "issue_resolved": true|false,
  "chat_complete": true|false,
  "issues": [],
  "quality_score": 0-100,
  "summary": "A clear 3–4 sentence explanation"
}}

Conversation:
{json.dumps(session_history, indent=2)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    if response.status_code != 200:
        raise ValueError(f"Ollama error {response.status_code}")

    data = response.json()

    if "response" not in data:
        raise ValueError("Invalid Ollama response")

    return extract_json(data["response"])


# ---------------- LOAD EXISTING ----------------

def load_existing():
    if not os.path.exists(OUTPUT_JSON):
        return []

    try:
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except:
        print("Existing JSON corrupted. Starting fresh.")
        return []


# ---------------- MAIN ----------------

def run_batch():

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        sessions = json.load(f)

    reports = load_existing()
    processed_ids = {r["session_id"] for r in reports if "session_id" in r}

    remaining = [s for s in sessions if s["session_id"] not in processed_ids]

    print(f"\nTotal sessions: {len(sessions)}")
    print(f"Already processed: {len(processed_ids)}")
    print(f"Remaining: {len(remaining)}\n")

    for i in range(0, len(remaining), BATCH_SIZE):

        batch = remaining[i:i+BATCH_SIZE]

        print(f"\nProcessing batch {i//BATCH_SIZE + 1} ({len(batch)} sessions)")

        for session in tqdm(batch):

            try:
                report = call_model(session["history"])

                report["session_id"] = session["session_id"]
                report["generated_at"] = datetime.utcnow().isoformat()

                reports.append(report)
                processed_ids.add(session["session_id"])

            except Exception as e:
                print(f"❌ Error on {session['session_id']}:", str(e))

                reports.append({
                    "session_id": session["session_id"],
                    "error": True,
                    "message": str(e),
                    "generated_at": datetime.utcnow().isoformat()
                })

                processed_ids.add(session["session_id"])

        # SAVE AFTER EVERY 100
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2)

        print(f"Batch saved ({len(processed_ids)}/{len(sessions)})")

    print("\nBatch processing complete.")


if __name__ == "__main__":
    run_batch()
