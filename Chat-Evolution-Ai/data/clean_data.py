import json

input_path = "data/processed_chat_turns.jsonl"
output_path = "data/clean_chat.json"

clean_records = []
skipped = 0

with open(input_path, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        try:
            record = json.loads(line)

            user_msg = record.get("user_message", "").strip()
            bot_msg = record.get("bot_message", "").strip()

            # Rule 1: user message empty → skip
            if user_msg == "":
                skipped += 1
                continue

            clean_records.append({
                "user_message": user_msg,
                "bot_message": bot_msg
            })

        except Exception as e:
            skipped += 1
            print(f"Skipped line {line_no}: {e}")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(clean_records, f, indent=2, ensure_ascii=False)

print("Cleaning completed")
print(f"Total clean records: {len(clean_records)}")
print(f"Total skipped records: {skipped}")
