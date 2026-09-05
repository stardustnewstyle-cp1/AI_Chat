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


# --- 7-1. analyze_input（意味軸スコア抽出） ---
def analyze_input(user_input: str, axes: dict) -> dict:
    """
    入力テキストから意味軸ごとのスコアを簡易に抽出する。
    キーワード＋構造でスコアを加算する。
    """
    text = user_input.lower()

    # キーワードベースの簡易ルール
    if any(k in text for k in ["構造", "structure", "章立て", "セクション"]):
        axes["structure"] += 1.0
        axes["organization"] += 0.5

    if any(k in text for k in ["手順", "procedure", "step", "やり方"]):
        axes["procedure"] += 1.0
        axes["action"] += 0.5

    if any(k in text for k in ["概念", "concept", "とは", "定義"]):
        axes["concept"] += 1.0
        axes["abstraction"] += 0.5

    if any(k in text for k in ["原因", "理由", "because", "why"]):
        axes["causality"] += 1.0

    if any(k in text for k in ["比較", "difference", "vs", "どっち", "違い"]):
        axes["contrast"] += 1.0
        axes["selection"] += 0.5

    if any(k in text for k in ["改善", "改善案", "optimize", "refactor", "better"]):
        axes["improvement"] += 1.0

    if any(k in text for k in ["整理", "まとめる", "構成", "organization"]):
        axes["organization"] += 1.0

    if any(k in text for k in ["選ぶ", "選択", "どれ", "select"]):
        axes["selection"] += 1.0

    if any(k in text for k in ["実行", "やる", "action", "動かす"]):
        axes["action"] += 1.0

    if any(k in text for k in ["抽象", "一般化", "パターン", "abstraction"]):
        axes["abstraction"] += 1.0

    return axes


# --- 7-2. classify_reasoning（推論タイプ分類） ---
def classify_reasoning(user_input: str) -> str:
    """
    入力テキストから推論タイプを決める。
    compare / improve / explain / organize / procedure / design などに近い分類。
    """
    text = user_input.lower()

    if any(k in text for k in ["比較", "difference", "vs", "どっち", "違い"]):
        return "comparative"

    if any(k in text for k in ["改善", "改善案", "optimize", "refactor", "better"]):
        return "improvement"

    if any(k in text for k in ["手順", "procedure", "step", "やり方"]):
        return "procedural"

    if any(k in text for k in ["構造", "structure", "章立て", "セクション"]):
        return "structural"

    if any(k in text for k in ["原因", "理由", "because", "why"]):
        return "causal"

    if any(k in text for k in ["概念", "concept", "とは", "定義"]):
        return "conceptual"

    if any(k in text for k in ["整理", "まとめる", "構成", "organization"]):
        return "organizational"

    if any(k in text for k in ["選ぶ", "選択", "どれ", "select"]):
        return "selective"

    return "structural"  # デフォルトは構造寄り


# --- 7-3. is_ambiguous（曖昧判定） ---
def is_ambiguous(user_input: str) -> bool:
    """
    曖昧かどうかを判定する。
    - 「なんでも」「適当に」などの曖昧語
    - 質問が漠然としている
    """
    text = user_input.lower()

    vague_patterns = [
        "なんでも",
        "適当に",
        "よしなに",
        "どうにかして",
        "いい感じに",
        "とりあえず",
        "ざっくり",
    ]
    if any(p in text for p in vague_patterns):
        return True

    # 文字数が極端に短い場合も曖昧とみなす
    if len(text.strip()) < 5:
        return True

    return False


# --- 7. Intent Layer（完成版） ---
def intent_layer(user_input):
    # 1. 意味軸初期化
    axes = init_axes()

    # 2. 意味解析
    axes = analyze_input(user_input, axes)

    # 3. 推論タイプ分類
    reasoning_type = classify_reasoning(user_input)

    # 4. direction_intent の生成
    direction = compute_direction_intent(axes, reasoning_type)

    # 5. 曖昧補正
    if is_ambiguous(user_input):
        direction = apply_fallback(direction)

    # 6. final_vector の生成
    final = compute_final_vector(direction)

    return {
        "axes": axes,
        "reasoning_type": reasoning_type,
        "direction": direction,
        "final_vector": final,
    }
