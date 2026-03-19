import re


DASH_VARIANTS = [
    "—",
    "–",
    "−",
    "-",
    "_"
]


def normalize_text(text: str) -> str:
    if not text:
        return ""
    for dash in DASH_VARIANTS:
        text = text.replace(dash, "-")
    text = re.sub(r"\s*-\s*", " - ", text)
    text = re.sub(r"[|•·]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return "\n".join(lines)