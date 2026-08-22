def apply_axis_fallback(axis_weight, text, features):
    """
    軸が全部弱い場合の安全補正。
    """

    if max(axis_weight.values()) < 0.3:
        axis_weight["logical"] += 0.5

    return axis_weight
