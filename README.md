# Sentifin — Real-Time Market Sentiment Analyzer

An end-to-end AI-powered market intelligence system that continuously ingests 
financial news and social media data, performs domain-adapted sentiment analysis 
using a fine-tuned transformer model, and surfaces actionable trading signals 
through a REST API and interactive dashboard.

Built as part of a research project exploring privacy-preserving NLP pipelines 
for multi-source financial data aggregation.

---

## Motivation

Retail investors face an overwhelming volume of unstructured financial text — 
news headlines, Reddit discussions, earnings commentary. Manually tracking 
sentiment across multiple sources for multiple stocks is infeasible. Sentifin 
automates this by running a continuous NLP pipeline that aggregates and 
interprets this data into clean, per-ticker signals.

---

## System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     Data Sources                        │
│         Reddit RSS          NewsAPI Headlines           │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
                ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Ingestion Pipeline                     │
│         Fetch → Clean → Normalize → Combine             │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Sentiment Model (LoRA RoBERTa)             │
│     Tokenize → Inference → Label + Confidence Score     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                Aggregation Engine                       │
│   Confidence-weighted scoring → BUY / HOLD / SELL       │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌──────────────┐    ┌─────────────────────────────────────┐
│   SQLite DB  │◄───│         Storage Layer               │
└──────────────┘    └─────────────────────────────────────┘
                          │
                ┌─────────┴──────────┐
                ▼                    ▼
        ┌──────────────┐    ┌────────────────┐
        │  FastAPI     │    │   Streamlit    │
        │  REST API    │    │   Dashboard    │
        └──────────────┘    └────────────────┘
```

---

## Key Features

- **Continuous data ingestion** from Reddit (r/stocks, r/investing, 
  r/wallstreetbets) and NewsAPI, refreshed automatically every hour
- **Domain-adapted sentiment model** — RoBERTa-base fine-tuned using LoRA 
  (Low-Rank Adaptation) on 11,000 financial tweets and Financial PhraseBank
- **Confidence-weighted signal aggregation** — per-ticker sentiment score 
  on a continuous scale from -1 (strongly bearish) to +1 (strongly bullish)
- **Actionable signal generation** — BUY / HOLD / SELL per ticker based on 
  aggregated sentiment
- **REST API** with FastAPI exposing sentiment data and signals per ticker
- **Interactive dashboard** with real-time sentiment breakdown, recent 
  headlines, and signal display per stock

---

## Model Details

| Property | Value |
|----------|-------|
| Base model | roberta-base |
| Fine-tuning method | LoRA (PEFT) |
| Training data | Financial PhraseBank + Financial Twitter (~11k samples) |
| Labels | Positive / Neutral / Negative |
| Eval Accuracy | 83.6% |
| Eval F1 | 83.7% |
| Eval Loss | 0.419 |

**Note on accuracy:** FinBERT, a model trained specifically on formal financial 
text, achieves ~87% on Financial PhraseBank alone. Our model is trained on a 
noisier combined dataset including social media text, making direct comparison 
non-trivial. The confidence-weighted aggregation layer mitigates individual 
prediction noise at scale.

---

## Research Background

This project builds on midterm research exploring federated learning for 
privacy-preserving sentiment aggregation across multiple data sources. Each 
data source (Reddit, news APIs) was treated as a separate federated client, 
with LoRA fine-tuning validated under federated simulation against centralized 
training baselines. The current implementation adopts a centralized architecture 
for the production pipeline while preserving the federated design as a planned 
extension.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Model | RoBERTa-base, LoRA via PEFT, PyTorch |
| NLP | HuggingFace Transformers |
| Backend | FastAPI, SQLite |
| Frontend | Streamlit |
| Ingestion | feedparser, NewsAPI |
| Training | Google Colab, LoRA (parameter-efficient fine-tuning) |

---

## Project Structure
```
sentifin/
├── ingestion/
│   ├── reddit_rss.py       # Reddit RSS ingestion via feedparser
│   ├── newsapi.py          # NewsAPI financial headlines ingestion
│   └── pipeline.py         # Combined multi-source ingestion
├── model/
│   ├── sentiment.py        # LoRA RoBERTa inference pipeline
│   └── aggregator.py       # Confidence-weighted signal generation
├── database/
│   └── db.py               # SQLite storage and retrieval
├── API/
│   └── main.py             # FastAPI REST endpoints
├── dashboard/
│   └── app.py              # Streamlit interactive dashboard
├── scheduler.py            # Automated hourly pipeline runner
├── config.py               # Configuration, API keys, constants
└── requirements.txt
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/tickers` | List of tracked tickers |
| GET | `/sentiment/{ticker}` | Recent sentiment records for a ticker |
| GET | `/signal/{ticker}` | Aggregated BUY/HOLD/SELL signal with score |

Full interactive API docs available at `http://localhost:8000/docs`

---

## Setup & Installation
```bash
# Clone the repository
git clone https://github.com/abhivsep1/Sentifin-Market-Analyzer.git
cd Sentifin-Market-Analyzer

# Install dependencies
pip install -r requirements.txt

# Configure config.py
NEWSAPI_KEY = "your_newsapi_key"
MODEL_PATH = "path/to/lora_roberta_finance"

# Run the automated pipeline scheduler
python scheduler.py

# Start the API (separate terminal)
cd API
uvicorn main:app --reload

# Start the dashboard (separate terminal)
streamlit run dashboard/app.py
```

---

## Tracked Tickers

TSLA · AAPL · NVDA · MSFT · AMZN

---

## Planned Improvements

- [ ] Stock price correlation via yfinance — validate signals against actual 
      price movement
- [ ] Sentiment trend visualisation over time
- [ ] Docker containerisation for portable deployment
- [ ] FinBERT vs RoBERTa comparative study
- [ ] Backtesting framework against historical price data
- [ ] Automated alerting when sentiment crosses threshold
- [ ] PostgreSQL migration for production scalability
- [ ] Federated learning integration across data source clients

---

## Limitations

- Reddit data obtained via RSS feeds due to API access restrictions — 
  full PRAW integration planned
- NewsAPI free tier limited to 100 requests/day
- Model trained on English financial text only
- Signal thresholds (±0.3) are heuristic — backtesting needed for validation
