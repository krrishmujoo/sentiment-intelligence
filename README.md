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

ML predicts. Python calculates. Claude plans. Python executes. Claude explains. Schemas constrain the boundaries.

Machine Learning

The sentiment classifier uses:

TF-IDF features
Unigrams and bigrams
Balanced Logistic Regression
Three sentiment classes:
Positive
Neutral
Negative

The training methodology uses a stratified 70 / 15 / 15 train-validation-test split.

The TF-IDF vectorizer is fitted only on the training split to avoid data leakage.

Multiple candidate models were evaluated, including:

Balanced Logistic Regression with unigram + bigram TF-IDF
Balanced Logistic Regression with unigram TF-IDF
Balanced LinearSVC
Unweighted Logistic Regression

The final model was selected using validation macro-F1, rather than accuracy alone, because the dataset is imbalanced and the neutral class is significantly harder to predict.

Locked test performance
Metric	Score
Accuracy	70.28%
Macro F1	63.63%
Weighted F1	70.88%
Negative F1	74.24%
Neutral F1	35.89%
Positive F1	80.76%

The neutral class remains the main weakness of the classifier.

One reason is that labels are derived from star ratings rather than manually annotated textual sentiment. Three-star reviews often contain mixed or ambiguous language.

This limitation is explicitly reflected in the system rather than hidden.

Uncertainty

The application does not treat every prediction as equally reliable.

For every prediction it calculates:

maximum class probability
top-two probability margin
confidence level
uncertainty flag

A prediction is currently marked uncertain when:

confidence < 0.60
OR
top1 probability - top2 probability < 0.10

These values are heuristic confidence signals and should not be interpreted as calibrated probabilities of correctness.

Local Review Analytics

Batch predictions are converted into deterministic analytics locally.

The analytics layer calculates:

sentiment counts
sentiment rates
average classifier confidence
uncertainty rate
theme-level sentiment
theme frequency
priority issues
Current theme taxonomy

The deterministic theme layer currently detects areas such as:

crashes
performance
login / authentication
payments
customer support
UI / UX
features
ads
notifications

The current implementation uses a lightweight keyword taxonomy.

This makes the layer inexpensive, deterministic, private, and easy to test, but it can miss semantic variations and occasionally produce keyword-matching false positives.

Semantic theme extraction is therefore a future improvement rather than something the current project claims to solve perfectly.

Priority Scoring

Issues are currently prioritized using:

priority_score =
frequency_share × negative_rate

This avoids automatically ranking a theme highly simply because one isolated mention is extremely negative.

The score is intentionally simple and interpretable.

It currently does not account for factors such as:

revenue impact
issue severity
customer segment value
trend velocity
product criticality

Those would be natural extensions for a production system with richer metadata.

Why use an LLM?

The LLM is not responsible for calculating sentiment statistics.

Instead, it is used in two constrained roles.

1. Analysis Planner

A user can ask:

“What are customers most unhappy about?”

Claude translates that question into a small set of approved analytical operations such as:

{
  "intent": "identify_top_customer_complaints",
  "operations": [
    {
      "operation": "filter_negative_themes",
      "limit": 5
    },
    {
      "operation": "rank_priority_issues",
      "limit": 5
    }
  ]
}

The planner may only select from a predefined operation registry.

Its output is validated using Pydantic before execution.

The LLM cannot execute arbitrary Python, shell commands, file operations, or database queries.

2. Business Insight Engine

After the validated plan is executed locally, the second LLM layer receives deterministic aggregate facts.

It produces:

an executive summary
data-grounded observations
recommended actions
recommendation priority

The UI explicitly separates:

Data-Grounded Observations

from

AI-Generated Recommendations

This prevents generated recommendations from being presented as measured statistics.

Privacy-Aware Design

A major design goal was avoiding the simplest architecture:

raw review dataset
      ↓
external LLM
      ↓
"analyze everything"

Instead, the aggregate intelligence workflow uses:

Raw reviews
    ↓
Local ML + analytics
    ↓
Privacy-safe aggregate representation
    ↓
LLM reasoning

The planner receives only:

the user's business question
descriptions of approved operations

The business insight engine receives only structured aggregate/executor facts.

The full raw review dataset is not sent to Claude in this workflow.

This is enforced structurally through the InsightPacket schema and tested automatically.

Technology Stack
Machine Learning
Python
pandas
NumPy
scikit-learn
TF-IDF
Logistic Regression
joblib
Backend
FastAPI
Pydantic
Uvicorn
AI Intelligence
Anthropic Claude
constrained planner
whitelisted operations
structured response validation
deterministic local executor
Frontend
React
TypeScript
Vite
Tailwind CSS
Recharts
Framer Motion
Lucide
Testing
pytest
FastAPI TestClient
Vitest
Playwright
Testing

The project includes automated tests across the ML, backend, analytics, LLM integration, and frontend layers.

Current full regression baseline:

114 tests passed

Coverage includes:

sentiment prediction
batch prediction
uncertainty logic
API validation
CSV parsing
analytics
theme extraction
priority scoring
privacy-safe InsightPacket construction
planner validation
unsafe operation rejection
planner executor
Claude planner adapter
Claude insight adapter
orchestration
/analyze
frontend behavior
end-to-end browser workflows

Anthropic calls are mocked in automated tests so test runs do not depend on external API availability or consume API credits.

Real integration calls were also tested separately during development.

Engineering Lessons

Several implementation issues shaped the final architecture.

Some examples include:

rebuilding a corrupted Python environment
preventing data leakage during model training
fixing duplicate Git repository initialization
migrating the frontend to React
stabilizing Playwright E2E tests
validating LLM-generated JSON
handling Markdown-wrapped model responses
handling multiple Anthropic content block types
distinguishing mocked API behavior from real integration behavior
handling external API connection failures
detecting truncated LLM responses using stop_reason
tuning output-token budgets
reducing unnecessary LLM verbosity

These failures were useful because they forced the system to become more explicit and defensive rather than relying on ideal API behavior.

Current Limitations

The current version deliberately has several known limitations:

Neutral sentiment remains difficult
Neutral F1 is significantly lower than positive and negative performance.
Theme extraction is keyword based
It does not yet provide semantic topic discovery.
Priority scoring is heuristic
It measures frequency and negativity but not business impact.
Sentiment probabilities are not calibrated
Confidence values should not be interpreted as true correctness probabilities.
Trend analysis requires richer metadata
Time, app version, region, customer segment, and product metadata would enable stronger analysis.
LLM token usage can be further optimized
Aggregate payload deduplication is a planned improvement.
Future Improvements

Potential extensions include:

semantic theme extraction
embedding-based clustering
transformer sentiment models
calibrated confidence scores
aspect-based sentiment analysis
trend analysis
app-version comparison
customer-segment analysis
richer business-priority models
reduced LLM token usage through compact aggregate payloads

The current version intentionally prioritizes a stable, interpretable, and testable architecture over adding every possible feature.

Running Locally
Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn src.api:app --reload --port 8000

FastAPI runs at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Environment

Create:

.env

and configure:

ANTHROPIC_API_KEY=your_key_here

Never commit .env.

Frontend
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173
API

Main endpoints:

GET  /health
POST /predict
POST /predict-batch
POST /analyze
Project Status

The current release contains the complete core sentiment and review-intelligence pipeline.

The next focus areas are:

production deployment
documentation refinement
LLM payload optimization
additional model/theme improvements

