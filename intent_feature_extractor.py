# ============================================
# feature_extractor.py
# Intent Layer 用：辞書抽出ロジック（強弱語・曖昧語・評価語）
# ============================================

import re
import json
import unicodedata

# --------------------------------------------
# 正規化
# --------------------------------------------
def normalize(text: str):
    # 全角→半角
    text = unicodedata.normalize("NFKC", text)
    # 小文字化
    text = text.lower()
    # 記号除去
    text = re.sub(r"[^\w\sぁ-んァ-ン一-龥]", " ", text)
    # 語尾揺れ統一
    replacements = {
        "したい": "する",
        "できますか": "する",
        "して": "する",
        "want to": "do",
        "can you": "do"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


# --------------------------------------------
# トークン化（英語＋日本語）
# --------------------------------------------
def tokenize(text: str):
    return re.findall(r"[a-zA-Z]+|[ぁ-んァ-ン一-龥]+", text)


# --------------------------------------------
# 辞書読み込み
# --------------------------------------------
def load_dict(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------
# 辞書抽出ロジック（Intent Layer の核）
# --------------------------------------------
def extract_features(text: str, dict_paths: dict):
    """
    dict_paths = {
        "strong": ".../strong.json",
        "medium": ".../medium.json",
        "weak": ".../weak.json",
        "vagueness": ".../vagueness.json",
        "evaluation": ".../evaluation.json",
        "concept": ".../concept.json",
        "contrast": ".../contrast.json"
    }
    """

    normalized = normalize(text)
    tokens = tokenize(normalized)

    # 辞書読み込み
    dicts = {k: load_dict(v) for k, v in dict_paths.items()}

    # 抽出結果
    result = {
        "strong": [],
        "medium": [],
        "weak": [],
        "vagueness": [],
        "evaluation": [],
        "concept": [],
        "contrast": [],
        "strength_score": 0.0,
        "raw": text
    }

    # ----------------------------------------
    # 辞書照合
    # ----------------------------------------
    for category, words in dicts.items():
        for w in words:
            if w in normalized:
                result[category].append(w)

    # ----------------------------------------
    # 強弱スコア計算
    # ----------------------------------------
    strong_count = len(result["strong"])
    medium_count = len(result["medium"])
    weak_count = len(result["weak"])

    score = (
        strong_count * 1.0 +
        medium_count * 0.6 +
        weak_count * 0.3
    ) / (len(tokens) + 1)

    result["strength_score"] = round(score, 3)

    return result
