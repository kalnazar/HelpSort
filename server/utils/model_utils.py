from pathlib import Path
import json

import joblib

from .preprocessing_utils import preprocessing_fn


# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent  # server/
MODELS_DIR = BASE_DIR / "models" / "model_schema" / "trained_models"

# TOPIC
TOPIC_MODEL_PATH = MODELS_DIR / "tfidf_topic" / "topic_tfidf_model.joblib"
TOPIC_LABELS_PATH = MODELS_DIR / "tfidf_topic" / "topic_label_map.json"

# PRIORITY
PRIORITY_MODEL_PATH = MODELS_DIR / "tfidf_priority" / "priority_tfidf_model.joblib"
PRIORITY_LABELS_PATH = MODELS_DIR / "tfidf_priority" / "priority_label_map.json"

# ROUTING
ROUTING_DIR = MODELS_DIR / "tfidf_routing"
ROUTING_MODEL_PATH = ROUTING_DIR / "model.pkl"
ROUTING_VECTORIZER_PATH = ROUTING_DIR / "vectorizer.pkl"
ROUTING_LABELS_PATH = ROUTING_DIR / "routing_labels.json"


def _load_labels(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if "labels" in meta:
        return meta["labels"]

    if "id2label" in meta:
        id2label = meta["id2label"]
        labels = [None] * len(id2label)
        for k, v in id2label.items():
            labels[int(k)] = v
        return labels

    if "label2id" in meta:
        label2id = meta["label2id"]
        labels = [None] * len(label2id)
        for label, idx in label2id.items():
            labels[int(idx)] = label
        return labels

    keys = list(meta.keys())
    if all(k.isdigit() for k in keys):
        labels = [None] * len(keys)
        for k, v in meta.items():
            labels[int(k)] = v
        return labels

    raise ValueError(f"Unsupported label map format in {path}")


# === Загрузка моделей при импорте ===

# TOPIC: pipeline + labels
topic_model = joblib.load(TOPIC_MODEL_PATH)
topic_labels = _load_labels(TOPIC_LABELS_PATH)

# PRIORITY: pipeline + labels
priority_model = joblib.load(PRIORITY_MODEL_PATH)
priority_labels = _load_labels(PRIORITY_LABELS_PATH)

# ROUTING: vectorizer + отдельная модель + labels
routing_vectorizer = joblib.load(ROUTING_VECTORIZER_PATH)
routing_model = joblib.load(ROUTING_MODEL_PATH)
routing_labels = _load_labels(ROUTING_LABELS_PATH)


def classify_all(raw_text: str) -> dict:
    """
    Классифицирует тикет сразу по трём измерениям:
      - topic
      - priority
      - routing (queue / отдел)

    Возвращает словарь:
    {
        "topic": "...",
        "topic_id": int,
        "priority": "...",
        "priority_id": int,
        "routing": "...",
        "routing_id": int
    }
    """
    # Базовая предобработка
    cleaned = preprocessing_fn(raw_text)

    # TOPIC — pipeline внутри сам сделает TF-IDF + predict
    topic_id = int(topic_model.predict([cleaned])[0])
    topic_label = topic_labels[topic_id]

    # PRIORITY
    priority_id = int(priority_model.predict([cleaned])[0])
    priority_label = priority_labels[priority_id]

    # ROUTING — тут векторизатор отдельно
    X_routing = routing_vectorizer.transform([cleaned])
    routing_id = int(routing_model.predict(X_routing)[0])
    routing_label = routing_labels[routing_id]

    return {
        "topic": topic_label,
        "topic_id": topic_id,
        "priority": priority_label,
        "priority_id": priority_id,
        "routing": routing_label,
        "routing_id": routing_id,
    }