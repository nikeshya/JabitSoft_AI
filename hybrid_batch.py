import json
import requests
import os
from datetime import datetime
from tqdm import tqdm

# ---------------- CONFIG ----------------

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

PRIMARY_MODEL = "qwen3:8b"
SECONDARY_MODEL = "llama3"

DATA_PATH = "clean_chat_history.json"
OUTPUT_JSON = "quality_reports_hybrid.json"
OUTPUT_CSV = "quality_reports_hybrid.csv"

BATCH_SIZE = 500  # change to 2 for testing

# ---------------- UTIL ----------------

def extract_json(text):
    if not text:
        raise ValueError("Empty response from model")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("Invalid JSON format from model")

    json_text = text[start:end + 1]
    return json.loads(json_text)


def call_model(model_name, session_history):
    prompt = f"""
You are an AI quality analyst.

Analyze the chatbot conversation and RETURN ONLY VALID JSON.

Return strictly:
{{
  "user_satisfaction": "high|medium|low",
  "bot_accuracy": "high|medium|low",
  "issue_resolved": true|false,
  "chat_complete": true|false,
  "issues": [],
  "quality_score": 0-100,
  "summary": "2–3 sentence explanation"
}}

Conversation:
{json.dumps(session_history, indent=2)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    if response.status_code != 200:
        raise ValueError(f"Ollama error: {response.status_code}")

    data = response.json()

    if "response" not in data:
        raise ValueError("Invalid Ollama response format")

    return extract_json(data["response"])


# ---------------- HYBRID CONDITION ----------------

def should_recheck(report):
    return (
        report.get("quality_score", 100) < 70
        or report.get("issue_resolved") is False
        or report.get("user_satisfaction") == "low"
    )


# ---------------- CSV SAVE ----------------

def save_csv(reports):
    headers = [
        "session_id",
        "model_used",
        "user_satisfaction",
        "bot_accuracy",
        "issue_resolved",
        "chat_complete",
        "quality_score",
        "summary",
        "generated_at"
    ]

    with open(OUTPUT_CSV, "w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        for r in reports:
            row = [str(r.get(h, "")).replace("\n", " ") for h in headers]
            f.write(",".join(f'"{x}"' for x in row) + "\n")


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
        print("⚠ Existing JSON corrupted. Starting fresh.")
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
                # PRIMARY MODEL
                report = call_model(PRIMARY_MODEL, session["history"])
                model_used = PRIMARY_MODEL

                # HYBRID RECHECK
                if should_recheck(report):
                    print(f"🔁 Rechecking {session['session_id']} with {SECONDARY_MODEL}")
                    report = call_model(SECONDARY_MODEL, session["history"])
                    model_used = SECONDARY_MODEL

                report["session_id"] = session["session_id"]
                report["model_used"] = model_used
                report["generated_at"] = datetime.utcnow().isoformat()

                reports.append(report)
                processed_ids.add(session["session_id"])

            except Exception as e:
                print(f"❌ Error on {session['session_id']}:", str(e))

                reports.append({
                    "session_id": session["session_id"],
                    "error": True,
                    "message": str(e),
                    "model_used": "error",
                    "generated_at": datetime.utcnow().isoformat()
                })

                # IMPORTANT FIX
                processed_ids.add(session["session_id"])

        # SAVE AFTER EACH BATCH
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2)

        save_csv(reports)

        print(f"✅ Batch saved ({len(processed_ids)}/{len(sessions)})")

    print("\n🎉 Hybrid processing complete.")


if __name__ == "__main__":
    run_batch()
