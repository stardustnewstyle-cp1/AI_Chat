# ============================================
# semantic_axes.py
# 意味軸分類ロジック（JSON辞書対応）
# ============================================

import json
import re
import unicodedata

# --------------------------------------------
# 正規化
# --------------------------------------------
def normalize(text: str):
    text = unicodedata.normalize("NFKC", text)
    return text.lower()

# --------------------------------------------
# トークン化（英語＋日本語）
# --------------------------------------------
def tokenize(text: str):
    return re.findall(r"[a-zA-Z]+|[ぁ-んァ-ン一-龥]+", text)

# --------------------------------------------
# JSON辞書読み込み
# --------------------------------------------
def load_axes_dict(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------
# 意味軸分類ロジック
# --------------------------------------------
def classify_axes(text: str, axes_dict: dict):
    normalized = normalize(text)
    tokens = tokenize(normalized)

    detected = {axis: [] for axis in axes_dict.keys()}

    for axis, keywords in axes_dict.items():
        for kw in keywords:
            if kw in normalized:
                detected[axis].append(kw)

    return {
        "axes": detected,
        "tokens": tokens,
        "raw": text
    }
