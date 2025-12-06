import re


def preprocessing_fn(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    # to lower
    text = text.lower()

    # remove simple HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # collapse multiple whitespace into single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()