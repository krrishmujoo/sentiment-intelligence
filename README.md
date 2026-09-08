# Sentiment Intelligence

**A privacy-aware review intelligence system that turns customer feedback into sentiment, recurring themes, prioritized issues, and business recommendations.**

Sentiment Intelligence started as a straightforward sentiment classification project, but a binary "positive or negative" label isn't what a product team actually needs. They need to know what customers are struggling with, which problems come up most often, which issues are worth prioritizing, how much to trust a given prediction, and what to do next.

This project answers those questions by combining a local machine learning classifier, deterministic analytics, constrained LLM planning, and AI-generated business insights into a single pipeline — with a hard boundary between the parts that compute facts and the parts that explain them.

---

## Table of Contents

- [What It Does](#what-it-does)
- [Architecture](#architecture)
- [Machine Learning](#machine-learning)
- [Uncertainty Detection](#uncertainty-detection)
- [Local Review Analytics](#local-review-analytics)
- [Why Use an LLM at All?](#why-use-an-llm-at-all)
- [Privacy-Aware Design](#privacy-aware-design)
- [Technology Stack](#technology-stack)
- [Testing](#testing)
- [Engineering Lessons](#engineering-lessons)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Project Status](#project-status)

---

## What It Does

- Single-review sentiment classification
- Batch review analysis
- CSV review import and prediction export
- Positive / neutral / negative classification
- Confidence and prediction-margin analysis
- Uncertainty detection
- Theme extraction and theme-level sentiment statistics
- Priority issue ranking
- Natural-language business questions over the review data
- Data-grounded observations, separated from AI-generated recommendations
- Privacy-aware LLM usage

**Example question:**

> What should the product team focus on first?

The system determines which approved analytics operations answer the question, calculates the underlying facts locally, and only then generates a business-facing explanation from those facts.

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
chooses approved analytics operations
       │
       ▼
Pydantic Validation
       │
       ▼
Local Planner Executor
calculates deterministic facts
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
```

**ML predicts. Python calculates. Claude plans. Python executes. Claude explains.** Schemas constrain the boundary at every handoff.

---

## Machine Learning

The sentiment classifier uses TF-IDF features (unigrams and bigrams) with a class-balanced Logistic Regression model, trained across three sentiment classes: positive, neutral, and negative.

The training methodology uses a stratified 70/15/15 train/validation/test split, and the TF-IDF vectorizer is fit only on the training split to avoid data leakage. Several candidate models were evaluated before selecting the final one:

- Balanced Logistic Regression with unigram + bigram TF-IDF
- Balanced Logistic Regression with unigram TF-IDF
- Balanced LinearSVC
- Unweighted Logistic Regression

The final model was selected using **validation macro-F1**, rather than accuracy alone, because the dataset is imbalanced and the neutral class is significantly harder to predict.

### Locked test performance

| Metric | Score |
|---|---|
| Accuracy | 70.28% |
| Macro F1 | 63.63% |
| Weighted F1 | 70.88% |
| Negative F1 | 74.24% |
| Neutral F1 | 35.89% |
| Positive F1 | 80.76% |

The neutral class remains the main weakness of the classifier. One reason is that labels are derived from star ratings rather than manually annotated textual sentiment — three-star reviews often contain mixed or ambiguous language. This limitation is reflected honestly in the system rather than hidden.

---

## Uncertainty Detection

The application does not treat every prediction as equally reliable. For every prediction, it calculates the maximum class probability, the top-two probability margin, a confidence level, and an uncertainty flag.

A prediction is currently marked uncertain when:

```text
confidence < 0.60
OR
top1_probability - top2_probability < 0.10
```

These values are heuristic confidence signals and should not be interpreted as calibrated probabilities of correctness.

---

## Local Review Analytics

Batch predictions are converted into deterministic analytics locally. The analytics layer calculates sentiment counts, sentiment rates, average classifier confidence, uncertainty rate, theme-level sentiment, theme frequency, and priority issues.

### Current theme taxonomy

The deterministic theme layer currently detects areas such as crashes, performance, login/authentication, payments, customer support, UI/UX, features, ads, and notifications, using a lightweight keyword taxonomy. This makes the layer inexpensive, deterministic, private, and easy to test — but it can miss semantic variations and occasionally produce keyword-matching false positives. Semantic theme extraction is a future improvement, not something the current project claims to solve.

### Priority scoring

Issues are prioritized using:

```text
priority_score = frequency_share × negative_rate
```

This avoids automatically ranking a theme highly simply because one isolated mention is extremely negative. The score is intentionally simple and interpretable, and does not currently account for revenue impact, issue severity, customer segment value, trend velocity, or product criticality — natural extensions for a production system with richer metadata.

---

## Why Use an LLM at All?

The LLM is never responsible for calculating sentiment statistics. It's used in two constrained roles.

### 1. Analysis Planner

A user can ask a question like *"What are customers most unhappy about?"* Claude translates that question into a small set of approved analytical operations:

```json
{
  "intent": "identify_top_customer_complaints",
  "operations": [
    { "operation": "filter_negative_themes", "limit": 5 },
    { "operation": "rank_priority_issues", "limit": 5 }
  ]
}
```

The planner may only select from a predefined operation registry, and its output is validated with Pydantic before execution. It cannot execute arbitrary Python, shell commands, file operations, or database queries.

### 2. Business Insight Engine

After the validated plan runs locally, a second LLM layer receives the deterministic aggregate facts and produces an executive summary, data-grounded observations, recommended actions, and a recommendation priority. The UI explicitly separates **data-grounded observations** from **AI-generated recommendations**, so a generated recommendation is never presented as a measured statistic.

---

## Privacy-Aware Design

A core design goal was avoiding the simplest architecture — raw review dataset straight into an external LLM with an "analyze everything" prompt. Instead, the workflow is:

```text
Raw reviews
    ↓
Local ML + analytics
    ↓
Privacy-safe aggregate representation
    ↓
LLM reasoning
```

The planner receives only the user's business question and descriptions of approved operations. The business insight engine receives only structured aggregate/executor facts. The full raw review dataset is never sent to Claude in this workflow — this is enforced structurally through the `InsightPacket` schema and covered by automated tests.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Machine Learning | Python, pandas, NumPy, scikit-learn, TF-IDF, Logistic Regression, joblib |
| Backend | FastAPI, Pydantic, Uvicorn |
| AI Intelligence | Anthropic Claude, constrained planner, whitelisted operations, structured response validation, deterministic local executor |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Recharts, Framer Motion, Lucide |
| Testing | pytest, FastAPI TestClient, Vitest, Playwright |

---

## Testing

The project includes automated tests across the ML, backend, analytics, LLM integration, and frontend layers.

**Current full regression baseline: 114 tests passed.**

Coverage includes sentiment prediction, batch prediction, uncertainty logic, API validation, CSV parsing, analytics, theme extraction, priority scoring, privacy-safe `InsightPacket` construction, planner validation, unsafe-operation rejection, the planner executor, the Claude planner and insight adapters, `/analyze` orchestration, frontend behavior, and end-to-end browser workflows.

Anthropic calls are mocked in automated tests so test runs don't depend on external API availability or consume API credits. Real integration calls were tested separately during development.

---

## Engineering Lessons

Several implementation issues shaped the final architecture, including:

- Rebuilding a corrupted Python environment
- Preventing data leakage during model training
- Fixing duplicate Git repository initialization
- Migrating the frontend to React
- Stabilizing Playwright end-to-end tests
- Validating LLM-generated JSON
- Handling Markdown-wrapped model responses
- Handling multiple Anthropic content block types
- Distinguishing mocked API behavior from real integration behavior
- Handling external API connection failures
- Detecting truncated LLM responses using `stop_reason`
- Tuning output-token budgets
- Reducing unnecessary LLM verbosity

These failures were useful — they forced the system to become more explicit and defensive rather than relying on ideal API behavior.

---

## Current Limitations

The current version deliberately has several known limitations:

- **Neutral sentiment remains difficult.** Neutral F1 is significantly lower than positive and negative performance.
- **Theme extraction is keyword-based.** It does not yet provide semantic topic discovery.
- **Priority scoring is heuristic.** It measures frequency and negativity, not business impact.
- **Sentiment probabilities are not calibrated.** Confidence values should not be interpreted as true correctness probabilities.
- **Trend analysis needs richer metadata.** Time, app version, region, customer segment, and product metadata would enable stronger analysis.
- **LLM token usage can be further optimized.** Aggregate payload deduplication is a planned improvement.

---

## Future Improvements

Potential extensions include semantic theme extraction, embedding-based clustering, transformer sentiment models, calibrated confidence scores, aspect-based sentiment analysis, trend analysis, app-version comparison, customer-segment analysis, richer business-priority models, and reduced LLM token usage through compact aggregate payloads.

The current version intentionally prioritizes a stable, interpretable, and testable architecture over adding every possible feature.

---

## Getting Started

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn src.api:app --reload --port 8000
```

FastAPI runs at `http://127.0.0.1:8000`, with interactive API docs at `http://127.0.0.1:8000/docs`.

### Environment

Create a `.env` file and configure:

```env
ANTHROPIC_API_KEY=your_key_here
```

Never commit `.env`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Single-review sentiment prediction |
| `POST` | `/predict-batch` | Batch review prediction |
| `POST` | `/analyze` | Natural-language business question → planned analysis → insights |

---

## Project Status

The current release contains the complete core sentiment and review-intelligence pipeline. Next focus areas: production deployment, documentation refinement, LLM payload optimization, and additional model/theme improvements.
