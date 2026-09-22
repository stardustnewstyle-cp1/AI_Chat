# feature_groups/selection_features.py
# ============================================================
# Selection（選択性）辞書
# ============================================================

SELECTION_FEATURES = {
    "selection": {
        "strong": [
            "select", "selection", "choose", "pick",
            "選ぶ", "選択", "選択する"
        ],
        "medium": [
            "choose from", "pick up", "候補から選ぶ"
        ],
        "weak": [
            "どれにする", "どれがいい"
        ]
    },

    "decision": {
        "strong": [
            "decide", "decision", "determine", "resolve",
            "決める", "決定", "意思決定"
        ],
        "medium": [
            "finalize", "確定する", "決めていく"
        ],
        "weak": [
            "どうする", "最終的に"
        ]
    },

    "criteria": {
        "strong": [
            "criteria", "standard", "condition", "requirement",
            "基準", "条件", "判断材料"
        ],
        "medium": [
            "rule", "指標", "選ぶ基準"
        ],
        "weak": [
            "ポイント", "見るところ"
        ]
    },

    "options": {
        "strong": [
            "option", "options", "alternative", "choice",
            "選択肢", "候補", "代替案"
        ],
        "medium": [
            "possibility", "可能性", "他の選択肢"
        ],
        "weak": [
            "どれがある", "何がある"
        ]
    },

    "determination": {
        "strong": [
            "determine", "determination", "settle", "conclude",
            "確定", "決め打ち", "最終決定"
        ],
        "medium": [
            "lock in", "固定する", "決めてしまう"
        ],
        "weak": [
            "決めるだけ", "確定させる"
        ]
    }
}
