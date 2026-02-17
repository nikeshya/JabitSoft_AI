# KL AI SYSTEM — Automated Chat Quality Scoring & Evaluation Framework

## Role in KL AI Roadmap

This system directly supports **Phase 2 — Intelligence Automation Layer** of the KL AI Development Roadmap.

| Roadmap Component | This System Covers |
|---|---|
| Hallucination Detector | ✔ Detects hallucinated responses per session |
| Response Validator | ✔ Validates JSON structure and response quality |
| Confidence Scoring | ✔ Quality score 0–100 per session |
| Self-Learning Loop | ✔ Identifies low-quality sessions for retraining |

---

## 1. System Overview

### Objective

Build an internal AI-powered automated chat quality scoring system that:

- Evaluates completed chatbot conversations
- Generates structured quality reports
- Produces summary analysis per session
- Works in batch + scheduled + on-demand modes
- Runs entirely on internal infrastructure using local LLMs

---

## 2. Current Implementation Summary

### Architecture Built

| Component | Implementation |
|---|---|
| Model Hosting | Local via Ollama |
| Primary Model | Qwen3:8B |
| Secondary Model | Llama3 (Hybrid Recheck) |
| Data Pipeline | Python batch processor |
| Scheduler | APScheduler / Cron |
| Storage | JSON + CSV persistent reporting |
| Deployment Mode | Manual + Daily Scheduled |
| Dataset Validated | 7,625 chat sessions |

---

## 3. Problem This System Solves

### Before

| Area | State |
|---|---|
| Quality Review | Manual, inconsistent |
| Scoring Mechanism | None |
| Daily Reporting | None |
| Per-Session Measurement | None |
| Hallucination Detection | None |
| Issue Tracking | None |

### After

| Area | State |
|---|---|
| Quality Review | Fully automated |
| Scoring Mechanism | Structured 0–100 scoring |
| Daily Reporting | Auto-generated JSON + CSV |
| Per-Session Measurement | Satisfaction + Accuracy tags |
| Hallucination Detection | Hybrid model revalidation |
| Issue Tracking | Categorized per session |

---

## 4. Architecture Overview

### Logical Flow

1. Chat completed
2. Stored in database / JSON
3. Scheduler triggers daily job
4. System filters chats by date
5. Hybrid evaluation pipeline runs
6. JSON structured report generated
7. Report appended to persistent storage

### Hybrid Evaluation Logic

| Layer | Model | Role |
|---|---|---|
| Primary | Qwen3:8B | Fast structured evaluation |
| Secondary | Llama3 | Deep recheck on flagged sessions |

### Recheck Trigger Conditions

| Condition | Threshold |
|---|---|
| Quality score | < 70 |
| Issue resolved | `false` |
| User satisfaction | `"low"` |

This prevents:

- False positives
- Inflated scoring
- Misclassification

---

## 5. Evaluation Output Format

Every session generates:

```json
{
  "session_id": "...",
  "user_satisfaction": "high|medium|low",
  "bot_accuracy": "high|medium|low",
  "issue_resolved": true|false,
  "chat_complete": true|false,
  "issues": [],
  "quality_score": 0-100,
  "summary": "...",
  "model_used": "...",
  "generated_at": "...",
  "report_date": "..."
}
```

This ensures:

- ✔ Structured output
- ✔ Automation compatibility
- ✔ Future analytics ready

---

## 6. Modes of Operation

| Mode | Description |
|---|---|
| Manual Date Mode | Evaluate any specific past date |
| Today Mode | Evaluate today's chats |
| Batch Mode | Process in configurable batches of 500 |
| Scheduled Mode | Automatically run daily at fixed time |

---

## 7. Automation Strategy

Scheduler configured using APScheduler:

- Runs daily at configured time (e.g., 11:30 PM)
- Filters chats by `created_at` date
- Generates report automatically
- Appends into master `quality_reports.json`

This removes:

- Manual monitoring
- Manual scoring
- Manual report compilation

---

## 8. Why Hybrid Model?

| Model | Strengths |
|---|---|
| Qwen3:8B | ✔ Strong JSON generation ✔ Stable reasoning ✔ Faster inference |
| Llama3 | ✔ Strong contextual correction ✔ Better on long/complex chats |

### Hybrid gives:

- ✔ Stability
- ✔ Safety fallback
- ✔ Improved scoring reliability
- ✔ Speed at scale with accuracy where it matters

---

## 9. Security & Data Privacy

| Area | Approach |
|---|---|
| Model Hosting | Internal server only (Ollama) |
| API Calls | Zero external calls |
| Data Storage | Local JSON, no cloud transfer |
| Compliance | No customer data leaves infrastructure |

---

## 10. Performance Characteristics

| Metric | Observed |
|---|---|
| JSON Accuracy | High |
| Hallucination Rate | Low |
| Inference Speed | Moderate |
| Hybrid Stability | Strong |
| Automation Reliability | High |
| Sessions Validated | 7,625 |

---

## 11. Integration Capability

System can integrate with:

- Live chat system
- CRM backend
- Post-chat trigger event
- Database write hook
- REST API endpoint (future extension)

Future integration possibility — event-driven trigger:

```
onChatCompleted(session_id):
    runEvaluation(session_id)
    storeReport()
```

---

## 12. Future Enhancements

| Phase | Enhancement |
|---|---|
| Phase 2 | Low score alert system |
| Phase 2 | Weekly aggregate analytics |
| Phase 2 | Dashboard visualization |
| Phase 3 | Confidence scoring layer |
| Phase 3 | Multi-thread batch acceleration |
| Phase 3 | Model fine-tuning on low-score sessions |

---

## 13. Strategic Impact

This system enables:

- ✔ Measurable AI performance tracking
- ✔ Reduced manual QA effort
- ✔ Scalable audit pipeline
- ✔ Continuous AI improvement
- ✔ Model benchmarking framework
- ✔ Foundation for future in-house SLM training

---

## 14. Final Vision Statement

The Automated Chat Quality Scoring System transforms chatbot monitoring from manual supervision into a **scalable, secure, AI-driven evaluation framework** built entirely on internal infrastructure — directly supporting KL AI's transition to a self-improving, private intelligence system.
