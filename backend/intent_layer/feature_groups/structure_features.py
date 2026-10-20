# feature_groups/structure_features.py
# ============================================================
# Structure（構造性）辞書
# ============================================================

STRUCTURE_FEATURES = {
    "components": {
        "strong": [
            "component", "module", "part", "要素", "部品", "コンポーネント"
        ],
        "medium": [
            "subsystem", "unit", "section", "セクション", "区分"
        ],
        "weak": [
            "もの", "部分"
        ]
    },

    "shape": {
        "strong": [
            "shape", "form", "構造", "形状", "フォーマット"
        ],
        "medium": [
            "pattern", "layout", "形式"
        ],
        "weak": [
            "見た目"
        ]
    },

    "relations": {
        "strong": [
            "relation", "dependency", "依存関係", "関連", "つながり"
        ],
        "medium": [
            "link", "connection", "関係性"
        ],
        "weak": [
            "関係"
        ]
    },

    "layout": {
        "strong": [
            "layout", "構成", "配置", "並び"
        ],
        "medium": [
            "arrangement", "structure"
        ],
        "weak": [
            "置き方"
        ]
    },

    "structuring": {
        "strong": [
            "structure", "構造化", "整理", "体系化"
        ],
        "medium": [
            "grouping", "分類"
        ],
        "weak": [
            "まとめ"
        ]
    }
}
