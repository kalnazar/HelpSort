import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.pipeline import Pipeline
import joblib

# пути к данным
TRAIN_PATH = "data/routing_train.csv"
VAL_PATH   = "data/routing_val.csv"

# куда сохраняем модель
MODEL_DIR = Path("server/models/model_schema/trained_models/tfidf_routing")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"
MODEL_PATH      = MODEL_DIR / "model.pkl"
LABELS_PATH     = MODEL_DIR / "routing_labels.json"


def main():
    print("Loading data...")
    train_df = pd.read_csv(TRAIN_PATH)
    val_df   = pd.read_csv(VAL_PATH)

    for col in ["text", "label"]:
        if col not in train_df.columns or col not in val_df.columns:
            raise ValueError("Columns 'text' and 'label' must exist in train/val CSV")

    # label mapping
    labels = sorted(train_df["label"].unique().tolist())
    label2id = {label: idx for idx, label in enumerate(labels)}
    id2label = {idx: label for label, idx in label2id.items()}

    y_train = train_df["label"].map(label2id)
    y_val   = val_df["label"].map(label2id)

    X_train = train_df["text"].astype(str)
    X_val   = val_df["text"].astype(str)

    print("Labels:", labels)

    # pipeline: TF-IDF + LogisticRegression
    print("Training routing model (TF-IDF + LogisticRegression)...")
    clf = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(
                max_features=30000,
                ngram_range=(1, 2),
                lowercase=True
            )),
            ("logreg", LogisticRegression(
                max_iter=1000,
                n_jobs=-1,
                class_weight="balanced"
            ))
        ]
    )

    clf.fit(X_train, y_train)

    # evaluate
    print("Evaluating on validation set...")
    y_pred = clf.predict(X_val)

    acc = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred, average="weighted")

    print(f"Accuracy: {acc:.4f}")
    print(f"Weighted F1: {f1:.4f}")
    print("\nClassification report:")
    print(classification_report(
        y_val, y_pred,
        target_names=[id2label[i] for i in range(len(labels))]
    ))

    # сохранить модель и маппинг
    print("Saving model and vectorizer...")
    # из pipeline вынимаем части, чтобы хранить отдельно (как в topic/priority)
    vectorizer = clf.named_steps["tfidf"]
    logreg     = clf.named_steps["logreg"]

    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(logreg, MODEL_PATH)

    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"labels": labels, "label2id": label2id, "id2label": id2label},
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Model saved to:", MODEL_DIR)


if __name__ == "__main__":
    main()