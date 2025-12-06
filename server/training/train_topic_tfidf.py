import pandas as pd
import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
import os

# Paths
TRAIN_PATH = "data/topic_train.csv"
VAL_PATH = "data/topic_val.csv"
LABELS_PATH = "server/config/topic_labels.json"
SAVE_DIR = "server/models/model_schema/trained_models/tfidf_topic"

os.makedirs(SAVE_DIR, exist_ok=True)

print("Loading data...")
train_df = pd.read_csv(TRAIN_PATH)
val_df = pd.read_csv(VAL_PATH)

# load label mapping for consistency
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict) and "labels" in data:
    labels = data["labels"]
else:
    labels = data

# Convert labels to numeric IDs
label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {idx: label for idx, label in enumerate(labels)}

train_df["label_id"] = train_df["label"].map(label2id)
val_df["label_id"] = val_df["label"].map(label2id)

# Build TF-IDF + Logistic Regression model
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=20000,
        ngram_range=(1,2),
        lowercase=True,
        stop_words="english"
    )),
    ("clf", LogisticRegression(max_iter=500))
])

print("Training model...")
model.fit(train_df["text"], train_df["label_id"])

print("Evaluating...")
preds = model.predict(val_df["text"])

acc = accuracy_score(val_df["label_id"], preds)
f1 = f1_score(val_df["label_id"], preds, average="weighted")

print("\nAccuracy:", acc)
print("Weighted F1:", f1)
print("\nClassification report:")
print(classification_report(val_df["label_id"], preds, target_names=labels))

# Save model + label mapping
joblib.dump(model, f"{SAVE_DIR}/topic_tfidf_model.joblib")

with open(f"{SAVE_DIR}/topic_label_map.json", "w", encoding="utf-8") as f:
    json.dump({
        "label2id": label2id,
        "id2label": id2label
    }, f, indent=2, ensure_ascii=False)

print(f"\nModel saved to: {SAVE_DIR}")
print("Training complete!")