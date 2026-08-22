def map_axis_to_reasoning(axis_weight):
    """
    最も強い軸から推論タイプを決定する。
    """

    strongest = max(axis_weight, key=axis_weight.get)

    mapping = {
        "technical": "reproduce_steps",
        "factual": "fact_priority",
        "logical": "logic_restructure",
        "causal": "cause_identification"
    }

    return mapping[strongest]
