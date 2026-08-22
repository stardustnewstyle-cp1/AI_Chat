# feature_groups/emotion_features.py
# ============================================================
# Emotion（感情性）辞書
# ============================================================

EMOTION_FEATURES = {
    "positive": {
        "strong": [
            "happy", "glad", "great", "awesome",
            "嬉しい", "最高", "良い", "便利"
        ],
        "medium": [
            "nice", "いい感じ", "助かる"
        ],
        "weak": [
            "ちょっと嬉しい", "まあ良い"
        ]
    },

    "negative": {
        "strong": [
            "bad", "terrible", "awful", "worst",
            "嫌だ", "悪い", "最悪", "ひどい"
        ],
        "medium": [
            "not good", "微妙", "よくない"
        ],
        "weak": [
            "ちょっと嫌", "あんまり"
        ]
    },

    "surprise": {
        "strong": [
            "surprised", "shocked", "unexpected",
            "驚いた", "まじで", "えっ", "予想外"
        ],
        "medium": [
            "びっくり", "意外"
        ],
        "weak": [
            "ちょっと驚き"
        ]
    },

    "confusion": {
        "strong": [
            "confused", "don't understand", "意味不明",
            "わからない", "混乱", "理解できない"
        ],
        "medium": [
            "よくわからん", "難しい"
        ],
        "weak": [
            "ちょっとわからん"
        ]
    },

    "frustration": {
        "strong": [
            "frustrated", "angry", "annoyed",
            "イライラ", "怒り", "なんでだよ", "ふざけんな"
        ],
        "medium": [
            "困る", "腹立つ", "ムカつく"
        ],
        "weak": [
            "ちょっとイラつく"
        ]
    }
}
