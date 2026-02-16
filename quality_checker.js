const OLLAMA_URL = "http://127.0.0.1:11434/api/generate";
const MODEL_NAME = "qwen3:8b";

function extractJSON(text) {
  if (!text) return null;
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1) return null;
  return text.slice(start, end + 1);
}

export async function analyzeSession(session) {
  try {
    const prompt = `
You are an AI quality analyst.

Analyze the chatbot conversation below and RETURN ONLY VALID JSON.

IMPORTANT RULES:
- "summary" MUST NOT be empty
- "summary" must clearly explain:
  1. What the user problem was
  2. What the assistant did
  3. Whether the problem was resolved

Return JSON strictly in this format:

{
  "user_satisfaction": "high|medium|low",
  "bot_accuracy": "high|medium|low",
  "issue_resolved": true|false,
  "chat_complete": true|false,
  "issues": [],
  "quality_score": 0-100,
  "summary": "A clear 2–3 sentence explanation of what happened in the chat"
}

Conversation:
${JSON.stringify(session.history, null, 2)}
`;

    const response = await fetch(OLLAMA_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: MODEL_NAME,
        prompt,
        stream: false
      })
    });

    const data = await response.json();
    const jsonText = extractJSON(data.response);

    if (!jsonText) {
      throw new Error("Invalid JSON from model");
    }

    const parsed = JSON.parse(jsonText);

    return {
      session_id: session.session_id,
      ...parsed
    };

  } catch (err) {
    return {
      session_id: session.session_id,
      error: true,
      message: err.message
    };
  }
}
