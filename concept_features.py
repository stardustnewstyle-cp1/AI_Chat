# feature_groups/concept_features.py
# ============================================================
# Concept（概念性）辞書
# ============================================================

CONCEPT_FEATURES = {
    "definition": {
        "strong": [
            "definition", "meaning", "what is", "とは", "定義", "意味"
        ],
        "medium": [
            "refers to", "stands for", "概要", "説明"
        ],
        "weak": [
            "って何", "何"
        ]
    },

    "characteristics": {
        "strong": [
            "feature", "characteristic", "property", "attribute", "特徴", "性質"
        ],
        "medium": [
            "behavior", "傾向", "特徴的"
        ],
        "weak": [
            "どんな"
        ]
    },

    "role": {
        "strong": [
            "role", "purpose", "function", "responsibility", "役割", "目的"
        ],
        "medium": [
            "use-case", "用途", "使い道"
        ],
        "weak": [
            "何のため"
        ]
    },

    "mechanism": {
        "strong": [
            "mechanism", "how it works", "仕組み", "動作", "内部"
        ],
        "medium": [
            "process", "流れ", "構造"
        ],
        "weak": [
            "どう動く"
        ]
    },

    "related_concepts": {
        "strong": [
            "related", "similar", "associated", "類似", "関連", "近い概念"
        ],
        "medium": [
            "belongs to", "category", "分類", "同じカテゴリ"
        ],
        "weak": [
            "違い", "比較"
        ]
    }
}
