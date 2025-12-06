import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

DATA_PATH = "data/aa_dataset-tickets-multi-lang-5-2-50-version.csv"

OUT_DIR = Path("data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = OUT_DIR / "routing_train.csv"
VAL_PATH   = OUT_DIR / "routing_val.csv"
TEST_PATH  = OUT_DIR / "routing_test.csv"


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    if "language" in df.columns:
        df = df[df["language"] != "de"].copy()

    required_cols = ["subject", "body", "queue"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in dataset")

    df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna("")).str.strip()
    df = df[df["text"] != ""].copy()

    df = df[["text", "queue"]].rename(columns={"queue": "label"})

    print("Total samples after filtering:", len(df))

    train_df, temp_df = train_test_split(
        df,
        test_size=0.3,
        random_state=42,
        stratify=df["label"]
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df["label"]
    )

    print("Train:", len(train_df), "Val:", len(val_df), "Test:", len(test_df))

    train_df.to_csv(TRAIN_PATH, index=False)
    val_df.to_csv(VAL_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)

    print("Saved:")
    print(" ", TRAIN_PATH)
    print(" ", VAL_PATH)
    print(" ", TEST_PATH)


if __name__ == "__main__":
    main()
