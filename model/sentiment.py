import sys
sys.path.insert(0, "D:/project_imp")

from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from config import MODEL_PATH, BASE_MODEL

LABELS = {0: "negative", 1: "neutral", 2: "positive"}

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL, num_labels=3)
model = PeftModel.from_pretrained(base_model, MODEL_PATH)
model.eval()

def predict(texts: list[str]) -> list[dict]:
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    results = []
    for i, text in enumerate(texts):
        pred = torch.argmax(probs[i]).item()
        results.append({
            "text": text,
            "label": LABELS[pred],
            "score": probs[i][pred].item()
        })
    return results