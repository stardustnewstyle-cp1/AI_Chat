# feature_groups/causality_features.py
# ============================================================
# Causality（因果性）辞書
# ============================================================

CAUSALITY_FEATURES = {
    "cause": {
        "strong": [
            "cause", "root cause", "原因", "要因", "根本原因"
        ],
        "medium": [
            "trigger", "きっかけ", "理由の一部"
        ],
        "weak": [
            "なんで", "どうして"
        ]
    },

    "effect": {
        "strong": [
            "effect", "result", "outcome", "結果", "影響"
        ],
        "medium": [
            "change", "変化", "影響が出る"
        ],
        "weak": [
            "こうなる"
        ]
    },

    "reason": {
        "strong": [
            "reason", "why", "理由", "なぜ", "理由として"
        ],
        "medium": [
            "because", "due to", "〜ため", "〜ので"
        ],
        "weak": [
            "なんでだろ"
        ]
    },

    "diagnosis": {
        "strong": [
            "diagnose", "diagnosis", "解析", "原因調査", "切り分け"
        ],
        "medium": [
            "investigate", "調査", "確認"
        ],
        "weak": [
            "見てみる"
        ]
    },

    "consequence": {
        "strong": [
            "consequence", "impact", "副作用", "影響範囲", "波及"
        ],
        "medium": [
            "follow-up", "後続", "続き"
        ],
        "weak": [
            "そのあと"
        ]
    }
}
