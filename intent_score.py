# intent_score.py

from typing import Dict

# あなたが設計した「意図ごとの重み」
INTENT_WEIGHTS = {
    "compare":      {"w1": 0.9, "w2": 0.7, "w3": 0.8, "w4": 0.4},
    "understand":   {"w1": 0.8, "w2": 0.9, "w3": 0.6, "w4": 0.3},
    "design":       {"w1": 0.7, "w2": 0.6, "w3": 0.9, "w4": 0.5},
    "debug":        {"w1": 0.6, "w2": 0.7, "w3": 0.8, "w4": 1.0},
    "improve":      {"w1": 0.7, "w2": 0.6, "w3": 0.9, "w4": 0.7},
    "optimize":     {"w1": 0.8, "w2": 0.6, "w3": 0.7, "w4": 0.6},
    "summarize":    {"w1": 0.9, "w2": 0.8, "w3": 0.4, "w4": 0.3},
    "generate":     {"w1": 0.8, "w2": 0.7, "w3": 0.5, "w4": 0.4},
    "classify":     {"w1": 0.7, "w2": 0.8, "w3": 0.6, "w4": 0.4},
    "evaluate":     {"w1": 0.6, "w2": 0.9, "w3": 0.7, "w4": 0.5},
}


def intent_score(features: Dict[str, float]) -> Dict[str, float]:
    """
    Intent のスコアを計算する（あなたの設計に完全準拠）
    features = {
        "keyword": float,
        "context": float,
        "structure": float,
        "source": float
    }
    """

    scores = {}

    for intent, w in INTENT_WEIGHTS.items():
        score = (
            features["keyword"]   * w["w1"] +
            features["context"]   * w["w2"] +
            features["structure"] * w["w3"] +
            features["source"]    * w["w4"]
        )

        # 正規化（0〜1）
        scores[intent] = min(score, 1.0)

    return scores
