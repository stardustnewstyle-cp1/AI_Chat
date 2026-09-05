# intent_layer/is_ambiguous.py

def is_ambiguous(text: str, axis_weight: dict, dict_features: dict) -> bool:
    """
    曖昧判定ロジック（Intent Layer 本番版）
    """

    # 1. vague（曖昧語）が多い
    vague_count = len(dict_features.get("vagueness", []))
    if vague_count >= 3:
        return True

    # 2. strong 語が少ない
    strong_count = len(dict_features.get("strong", []))
    if strong_count == 0:
        return True

    # 3. axis_weight の最大値が低い（どの軸も弱い）
    max_axis = max(axis_weight.values())
    if max_axis < 0.2:
        return True

    # 4. axis_weight の分布が均等（差が小さい）
    sorted_weights = sorted(axis_weight.values(), reverse=True)
    if sorted_weights[0] - sorted_weights[1] < 0.05:
        return True

    # 5. concept_density が低い（語彙が少ない）
    if dict_features.get("concept_density", 0) < 0.05:
        return True

    # 6. connectives が少ない（論理構造が弱い）
    if dict_features.get("connectives", 0) == 0:
        return True

    # 7. semantic_axes の一致が少ない
    axes_hits = sum(len(v) for v in dict_features.get("concept", []))
    if axes_hits == 0:
        return True

    return False
