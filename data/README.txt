Dataset overview

This folder contains CSV files used to train and validate the TF‑IDF classifiers. The repository includes examples of topic, priority and routing datasets.

Files (examples):
- `data/topic_train.csv`, `data/topic_val.csv`
- `data/priority_train.csv`, `data/priority_val.csv`
- `data/routing_train.csv`, `data/routing_val.csv`

Expected CSV schema
- `text` — the ticket text (string). Should be UTF-8 encoded.
- `label` — the target label (string) for the given task. For topic/priority/routing the label values must match those in `server/config/*.json` or the training scripts will map labels to IDs.

Preprocessing
- A minimal cleaning is applied by `server/utils/preprocessing_utils.py` (lowercasing, strip HTML tags, collapse whitespace). If you need additional preprocessing (stemming, stopword removal, language-specific tokenization) add it before training.
- For routing data there is a helper `server/training/prepare_routing_data.py` — inspect and run that script when preparing routing datasets.

Languages and size
- The datasets include mainly English samples and a smaller portion of Kazakh. File sizes and exact counts vary by dataset — inspect CSVs with `wc -l data/*.csv` or open them in a spreadsheet editor.

Notes
- Do not commit large or sensitive data to the repository. Use external storage or data versioning tools for large datasets.
- If you regenerate datasets or retrain models, run the training scripts in `server/training/`.

If you'd like, I can add a small `data/inspect.py` script to print basic stats (rows per label, sample counts) for each CSV.
