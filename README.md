# Sentiment Intelligence

**A privacy-aware customer feedback intelligence platform that turns reviews into sentiment, recurring themes, prioritized issues, and business recommendations.**

Sentiment Intelligence started as a traditional sentiment classification project, but I wanted to answer a more useful question than simply *“Is this review positive or negative?”*

Product teams usually want to know:

- What are customers struggling with?
- Which problems appear most often?
- Which issues should be prioritized?
- How confident is the model in its predictions?
- What actions should the team consider next?

The project therefore evolved into an end-to-end review intelligence system combining **local machine learning, deterministic analytics, constrained LLM planning, and AI-generated business insights.**

---

## What the system does

The application supports:

- Single-review sentiment classification
- Batch review analysis
- CSV review import and prediction export
- Positive / neutral / negative classification
- Confidence and prediction-margin analysis
- Uncertainty detection
- Theme extraction
- Theme-level sentiment statistics
- Priority issue ranking
- Natural-language business questions
- Data-grounded observations
- AI-generated recommendations
- Privacy-aware LLM usage

### Example question

> **What should the product team focus on first?**

The system determines which approved analytics operations are needed, calculates the underlying facts locally, and then generates a business-facing explanation from those facts.

---

## Architecture

The project deliberately separates **prediction, calculation, planning, and explanation**.

```text
Customer Reviews
       │
       ▼
Local Sentiment Model
TF-IDF + Logistic Regression
       │
       ▼
Predictions + Confidence + Uncertainty
       │
       ▼
Local Analytics Engine
       │
       ├── Sentiment distribution
       ├── Theme statistics
       ├── Uncertainty metrics
       └── Priority scoring
       │
       ▼
Privacy-Safe InsightPacket
       │
       ▼
Claude Planner
       │
       ▼
Pydantic Validation
       │
       ▼
Local Planner Executor
       │
       ▼
Claude Insight Engine
       │
       ├── Executive summary
       ├── Data-grounded observations
       └── Recommended actions
       │
       ▼
React Dashboard