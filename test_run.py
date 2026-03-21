import sys
sys.path.insert(0, "D:/project_imp")

from I    ngestion.pipeline import run_ingestion
from model.sentiment import predict
from database.db import init_db, insert_results, get_sentiment_by_ticker

# Step 1: initialize database
print("initializing database...")
init_db()
print("database ready")

# Step 2: fetch data
print("\nfetching data...")
raw = run_ingestion()
print(f"fetched {len(raw)} items")

# Step 3: run model on all items
print("\nrunning inference...")
texts = [item["text"] for item in raw]
preds = predict(texts)

# Step 4: merge predictions back into raw data
for i, item in enumerate(raw):
    item["label"] = preds[i]["label"]
    item["score"] = preds[i]["score"]

# Step 5: store in database
print("\nstoring results...")
insert_results(raw)
print("stored successfully")

# Step 6: verify by reading back
print("\nverifying — TSLA results from database:")
rows = get_sentiment_by_ticker("TSLA")
print(f"found {len(rows)} TSLA records")
print("\nFirst 3 rows:")
for row in rows[:3]:
    print(row)