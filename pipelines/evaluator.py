# ============================================
# evaluator.py（意味軸対応版）
# ============================================

import re

class Evaluator:

    def evaluate(self, article, axes=None, reasoning_type=None):
        """
        意味軸（axes）と推論タイプ（reasoning_type）に応じて
        評価観点を切り替える強化版 Evaluator
        """

        axes = axes or {}
        reasoning_type = reasoning_type or "structural"

        results = []

        # -----------------------------
        # 1. structure（構造評価）
        # -----------------------------
        if axes.get("structure", 0) > 0.6 or reasoning_type == "structural":
            results.append(self._eval_structure(article))

        # -----------------------------
        # 2. procedure（手順評価）
        # -----------------------------
        if axes.get("procedure", 0) > 0.6 or reasoning_type == "procedural":
            results.append(self._eval_procedure(article))

        # -----------------------------
        # 3. concept（概念評価）
        # -----------------------------
        if axes.get("concept", 0) > 0.6 or reasoning_type == "conceptual":
            results.append(self._eval_concept(article))

        # -----------------------------
        # 4. example（例評価）
        # -----------------------------
        if axes.get("example", 0) > 0.6:
            results.append(self._eval_example(article))

        # -----------------------------
        # 5. explain（説明評価）
        # -----------------------------
        if axes.get("explain", 0) > 0.6 or reasoning_type == "causal":
            results.append(self._eval_explain(article))

        # -----------------------------
        # 6. notes（注意点評価）
        # -----------------------------
        if axes.get("notes", 0) > 0.6 or reasoning_type == "improvement":
            results.append(self._eval_notes(article))

        # -----------------------------
        # 7. fallback（構造評価）
        # -----------------------------
        if not results:
            results.append(self._eval_structure(article))

        return results

    # =========================================================
    # 各評価観点の実装
    # =========================================================

    def _eval_structure(self, article):
        score = 0
        if "#" in article:
            score += 0.5
        if re.search(r"(まとめ|結論|ポイント)", article):
            score += 0.5

        return {
            "type": "structure",
            "score": score,
            "comment": "構造化されているかを評価しました。"
        }

    def _eval_procedure(self, article):
        steps = len(re.findall(r"(Step|手順|まず|次に|最後に)", article))
        score = min(1.0, steps / 5)

        return {
            "type": "procedure",
            "score": score,
            "comment": "手順の明確さを評価しました。"
        }

    def _eval_concept(self, article):
        concepts = len(re.findall(r"(とは|定義|概念)", article))
        score = min(1.0, concepts / 3)

        return {
            "type": "concept",
            "score": score,
            "comment": "概念の明確さを評価しました。"
        }

    def _eval_example(self, article):
        examples = len(re.findall(r"(例|ケース|サンプル)", article))
        score = min(1.0, examples / 3)

        return {
            "type": "example",
            "score": score,
            "comment": "例の適切さを評価しました。"
        }

    def _eval_explain(self, article):
        explains = len(re.findall(r"(理由|なぜ|because|説明)", article))
        score = min(1.0, explains / 3)

        return {
            "type": "explain",
            "score": score,
            "comment": "説明の十分さを評価しました。"
        }

    def _eval_notes(self, article):
        notes = len(re.findall(r"(注意|警告|危険|重要)", article))
        score = min(1.0, notes / 3)

        return {
            "type": "notes",
            "score": score,
            "comment": "注意点の適切さを評価しました。"
        }
