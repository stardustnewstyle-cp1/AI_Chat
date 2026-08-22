def extract_axis_weights(text, features):
    """
    Semantic Axes（意味軸）の重みを抽出する。
    """

    axes = {
        "technical": 0.0,
        "logical": 0.0,
        "factual": 0.0,
        "causal": 0.0
    }

    # technical 軸
    if any(w in text for w in ["手順", "方法", "ステップ"]):
        axes["technical"] += 0.7

    # logical 軸
    if any(w in text for w in ["整理", "構造", "論理"]):
        axes["logical"] += 0.7

    # factual 軸
    if any(w in text for w in ["事実", "データ", "数値"]):
        axes["factual"] += 0.7

    # causal 軸
    if any(w in text for w in ["原因", "理由", "なぜ"]):
        axes["causal"] += 0.7

    # 特徴量による補正
    axes["technical"] += features["structure_strength"] * 0.1
    axes["factual"] += features["keyword_strength"] * 0.05

    return axes
