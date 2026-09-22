# intent_layer/classify_reasoning.py

from intent_layer.intent_layer import REASONING_TYPES

def classify_reasoning(axis_weight: dict) -> str:
    """
    意味軸の重みに基づいて推論タイプを決定する。
    """

    reasoning_scores = {}

    # 各推論タイプの軸重みを合計
    for rtype, axes in REASONING_TYPES.items():
        score = sum(axis_weight.get(axis, 0.0) for axis in axes)
        reasoning_scores[rtype] = score

    # 最も強い推論タイプを選択
    best_type = max(reasoning_scores, key=reasoning_scores.get)

    # 推論タイプ名を Intent Layer の正式名に変換
    mapping = {
        "comparative": "compare",
        "causal": "debug",
        "improvement": "improve",
        "procedural": "optimize",
        "conceptual": "design",
        "structural": "design",
        "organizational": "design",
        "selective": "classify"
    }

    return mapping.get(best_type, "unknown")
