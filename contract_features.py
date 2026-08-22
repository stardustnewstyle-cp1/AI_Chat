# feature_groups/contrast_features.py
# ============================================================
# Contrast（対比性）辞書
# ============================================================

CONTRAST_FEATURES = {
    "difference": {
        "strong": [
            "difference", "different", "違い", "差分", "相違点"
        ],
        "medium": [
            "distinct", "区別", "差がある"
        ],
        "weak": [
            "どっちが違う", "違うの？"
        ]
    },

    "similarity": {
        "strong": [
            "similar", "similarity", "類似", "似ている", "共通点"
        ],
        "medium": [
            "close to", "近い", "似たような"
        ],
        "weak": [
            "なんとなく似てる"
        ]
    },

    "advantage": {
        "strong": [
            "advantage", "benefit", "メリット", "利点", "強み"
        ],
        "medium": [
            "good point", "良いところ"
        ],
        "weak": [
            "いい感じ"
        ]
    },

    "disadvantage": {
        "strong": [
            "disadvantage", "weakness", "デメリット", "欠点", "弱点"
        ],
        "medium": [
            "bad point", "悪いところ"
        ],
        "weak": [
            "微妙"
        ]
    },

    "comparison": {
        "strong": [
            "compare", "comparison", "比較", "対比", "比べる"
        ],
        "medium": [
            "versus", "vs", "〜と〜の比較"
        ],
        "weak": [
            "どっち", "どれがいい"
        ]
    }
}
