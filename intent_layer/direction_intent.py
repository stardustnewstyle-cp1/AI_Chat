# direction_intent.py

import math

def normalize(value):
    # value は float の合計値
    return value if value == 0 else value / (abs(value) + 1e-9)


def direction_intent(axes):
    """
    axes は Semantic Axes の出力（辞書）
    例：
    axes = {
        "action": 0.2,
        "procedure": 0.8,
        "abstraction": 0.4,
        "structure": 0.6,
        "reasoning": 0.3,
        "organization": 0.7,
        "grouping": 0.5,
        "concept": 0.9,
        "progression": 0.4,
        "contrast": 0.2,
        "improvement": 0.1,
        "analysis": 0.5,
        "selection": 0.3,
        "causality": 0.6
    }
    """

    directions = {}

    # Implementation
    directions["implementation"] = normalize(
        axes["action"] + axes["procedure"]
    )

    # Design（抽象化・構造・思考）
    directions["design"] = normalize(
        axes["abstraction"] * 0.6 +
        axes["structure"] * 0.4 +
        axes["reasoning"] * 0.3
    )

    # Structuring（整理・分類・構造）
    directions["structuring"] = normalize(
        axes["organization"] * 0.7 +
        axes["grouping"] * 0.5 +
        axes["structure"] * 0.2
    )

    # Understanding（深い理解）
    directions["understanding"] = normalize(
        axes["concept"] * 0.7 +
        axes["abstraction"] * 0.5 +
        axes["reasoning"] * 0.4
    )

    # Learning（学習プロセス）
    directions["learning"] = normalize(
        axes["concept"] * 0.3 +
        axes["organization"] * 0.6 +
        axes["procedure"] * 0.5 +
        axes["progression"] * 0.4
    )

    # Debug（原因追跡）
    directions["debug"] = normalize(
        axes["causality"] + axes["procedure"]
    )

    # Comparison（比較）
    directions["comparison"] = normalize(
        axes["contrast"]
    )

    # Optimization（改善）
    directions["optimization"] = normalize(
        axes["improvement"]
    )

    # Evaluation（評価）
    directions["evaluation"] = normalize(
        axes["analysis"] * 0.6 +
        axes["concept"] * 0.4
    )

    # Decision（選択＋思考）
    directions["decision"] = normalize(
        axes["selection"] * 0.7 +
        axes["reasoning"] * 0.3
    )

    return directions
