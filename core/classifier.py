# classifier.py

class Classifier:
    """
    Intent Layer が返す axes（意味軸の強度）を使って
    記事カテゴリを分類する本番用分類器。
    """

    def classify(self, article: str, axes: dict) -> str:
        # axes は Intent Layer が返す意味軸の強度
        # 例: {"structure": 0.8, "comparison": 0.2, "debug": 0.1, ...}

        if not axes:
            return "general"

        # 最も強い意味軸をカテゴリとして採用
        strongest_axis = max(axes, key=lambda k: axes[k])
        strength = axes[strongest_axis]

        # 閾値でカテゴリを調整（弱い場合は general）
        if strength < 0.25:
            return "general"

        # 軸名をカテゴリ名として返す
        return strongest_axis
