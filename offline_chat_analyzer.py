from sentence_transformers import SentenceTransformer
import numpy as np

class RAGIndex:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.user_queries = []
        self.bot_replies = []
        self.embeddings = None

    def build(self, sessions):
        for sess in sessions.values():
            for i in range(len(sess) - 1):
                if sess[i]["speaker"] == "user" and sess[i + 1]["speaker"] == "bot":
                    bot_msg = sess[i + 1]["message"].strip().lower()
                    if bot_msg and "error" not in bot_msg:
                        self.user_queries.append(sess[i]["message"])
                        self.bot_replies.append(sess[i + 1]["message"])

        if self.user_queries:
            self.embeddings = self.model.encode(self.user_queries)

    def retrieve_best_reply(self, query):
        if self.embeddings is None:
            return "Thank you for your query. Please provide more details so I can help you."

        q_emb = self.model.encode([query])[0]
        sims = np.dot(self.embeddings, q_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(q_emb)
        )
        best_idx = int(np.argmax(sims))
        return self.bot_replies[best_idx]
