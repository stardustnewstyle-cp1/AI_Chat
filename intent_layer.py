# intent_layer.py

# ============================
# SAMLRM — Intent Layer
# ============================

# --- 1. 意味軸（10軸） ---
SEMANTIC_AXES = {
    "structure": 0.0,
    "procedure": 0.0,
    "concept": 0.0,
    "causality": 0.0,
    "contrast": 0.0,
    "improvement": 0.0,
    "organization": 0.0,
    "selection": 0.0,
    "action": 0.0,
    "abstraction": 0.0
}

def init_axes():
    return {axis: 0.0 for axis in SEMANTIC_AXES}


# --- 2. 推論タイプ（8種類） ---
REASONING_TYPES = {
    "structural": ["structure", "organization"],
    "procedural": ["procedure", "action"],
    "conceptual": ["concept", "abstraction"],
    "causal": ["causality"],
    "comparative": ["contrast"],
    "improvement": ["improvement"],
    "organizational": ["organization"],
    "selective": ["selection"]
}

def apply_reasoning_type(axes, reasoning_type, weight=1.0):
    if reasoning_type not in REASONING_TYPES:
        return axes
    for axis in REASONING_TYPES[reasoning_type]:
        axes[axis] += weight
    return axes


# --- 3. 正規化 ---
def normalize_axes(axes):
    total = sum(axes.values())
    if total == 0:
        return axes
    return {axis: value / total for axis, value in axes.items()}


# --- 4. fallback（曖昧補正） ---
def apply_fallback(vector):
    safe_axes = ["structure", "concept", "organization"]
    for axis in safe_axes:
        vector[axis] += 0.5
    return vector


# --- 5. direction_intent（推論方向ベクトル） ---
def compute_direction_intent(user_axes, reasoning_type):
    axes = user_axes.copy()
    axes = apply_reasoning_type(axes, reasoning_type, weight=1.0)
    return axes


# --- 6. final_vector（正規化） ---
def compute_final_vector(direction_intent):
    return normalize_axes(direction_intent)


# --- 7. Intent Layer（完成版） ---
def intent_layer(user_input):
    # 1. 意味軸初期化
    axes = init_axes()

    # 2. 意味解析（あなたが思想を決める部分）
    axes = analyze_input(user_input, axes)

    # 3. 推論タイプ分類（あなたが思想を決める部分）
    reasoning_type = classify_reasoning(user_input)

    # 4. direction_intent の生成
    direction = compute_direction_intent(axes, reasoning_type)

    # 5. 曖昧補正
    if is_ambiguous(user_input):
        direction = apply_fallback(direction)

    # 6. final_vector の生成
    final = compute_final_vector(direction)

    return final
