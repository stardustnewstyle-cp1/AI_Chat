# ============================
# SAMLRM — Intent Layer.py
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


# --- 追加①：技術質問判定 ---
def is_technical(text: str) -> bool:
    tech_keywords = [
        "api", "関数", "コード", "python", "javascript",
        "エラー", "例外", "最適化", "設計", "アルゴリズム",
        "クラス", "メソッド", "ライブラリ", "フレームワーク",
        "引数", "戻り値", "型", "オブジェクト", "インスタンス"
    ]
    t = text.lower()
    return any(k in t for k in tech_keywords)


# --- 追加②：技術回答用の意味軸 ---
def extract_technical_axes(text: str) -> dict:
    axes = {
        "code": 0.0,
        "example": 0.0,
        "explain": 0.0,
        "notes": 0.0,
        "design": 0.0
    }

    t = text.lower()

    if "コード" in t or "書いて" in t or "実装" in t:
        axes["code"] = 0.9

    if "例" in t or "サンプル" in t or "example" in t:
        axes["example"] = 0.7

    if "説明" in t or "どういう" in t or "why" in t:
        axes["explain"] = 0.6

    if "注意" in t or "気をつけ" in t:
        axes["notes"] = 0.5

    if "設計" in t or "構造" in t or "architecture" in t:
        axes["design"] = 0.8

    return axes


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
    text = user_input.lower()

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

    return "structural"


# --- 7-3. is_ambiguous（曖昧判定） ---
def is_ambiguous(user_input: str) -> bool:
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

    if len(text.strip()) < 5:
        return True

    return False


# --- 7. Intent Layer（完成版） ---
def intent_layer(user_input):
    axes = init_axes()
    axes = analyze_input(user_input, axes)
    reasoning_type = classify_reasoning(user_input)
    direction = compute_direction_intent(axes, reasoning_type)

    if is_ambiguous(user_input):
        direction = apply_fallback(direction)

    final = compute_final_vector(direction)

    technical = is_technical(user_input)
    axes_tech = extract_technical_axes(user_input) if technical else {}

    return {
        "technical": technical,
        "axes": axes,
        "axes_tech": axes_tech,
        "reasoning_type": reasoning_type,
        "direction": direction,
        "final_vector": final,
    }
