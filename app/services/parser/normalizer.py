import re


DASH_VARIANTS = [
    "—",
    "–",
    "−",
    "-"
]


def normalize_text(text: str) -> str:
    if not text:
        return ""
    for dash in DASH_VARIANTS:
        text = text.replace(dash, "-")
    text = re.sub(r"\s*-\s*", " - ", text)
    text = re.sub(r"[|•·]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace('0', 'О')
    text = text.replace('1', 'І')
    # text = re.sub(r'([а-яА-ЯёЁ])\1{2,}', r'\1', text)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return "\n".join(lines)