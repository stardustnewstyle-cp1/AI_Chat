# intent_layer/analyze_input.py

from intent_layer.feature_extractor import extract_features as dict_extract
from intent_layer.feature_loader import FEATURE_GROUPS
from intent_layer.semantic_axes import classify_axes
from intent_layer.axis_extractor import extract_axis_weights as simple_axes

def analyze_input(text: str, axes: dict) -> dict:
    # 1. semantic_axes.json の軸検出
    axes_detected = classify_axes(text, axes)["axes"]

    # 2. feature_groups の強弱語抽出
    detected_features = dict_extract(text, FEATURE_GROUPS)

    # 3. 簡易軸（technical / logical / factual / causal）
    simple = simple_axes(text, {
        "structure_strength": 0,
        "keyword_strength": 0
    })

    # 4. 軸重み計算
    axis_weight = {axis: 0.0 for axis in axes.keys()}

    # --- semantic_axes.json の一致数 ---
    for axis, words in axes_detected.items():
        axis_weight[axis] += len(words) * 1.0

    # --- feature_groups の強弱語 ---
    for axis, items in detected_features.items():
        for subcategory, word in items:
            if subcategory == "strong":
                axis_weight[axis] += 1.0
            elif subcategory == "medium":
                axis_weight[axis] += 0.6
            elif subcategory == "weak":
                axis_weight[axis] += 0.3

    # --- 簡易軸を semantic_axes にマッピング ---
    axis_weight["procedure"] += simple["technical"]
    axis_weight["structure"] += simple["logical"]
    axis_weight["concept"] += simple["factual"]
    axis_weight["causality"] += simple["causal"]

    # --- 正規化 ---
    total = sum(axis_weight.values())
    if total > 0:
        axis_weight = {k: v / total for k, v in axis_weight.items()}

    return axis_weight
