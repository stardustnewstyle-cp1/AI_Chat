# ============================================
# summarizer.py（意味軸対応版）
# ============================================

import re

class Summarizer:

    def summarize(self, article, template, axes=None, reasoning_type=None):
        """
        意味軸（axes）と推論タイプ（reasoning_type）に応じて
        要約スタイルを切り替える強化版 Summarizer
        """

        axes = axes or {}
        reasoning_type = reasoning_type or "structural"

        # -----------------------------
        # 1. structure（構造化要約）
        # -----------------------------
        if axes.get("structure", 0) > 0.6 or reasoning_type == "structural":
            return self._summarize_structure(article)

        # -----------------------------
        # 2. procedure（手順中心）
        # -----------------------------
        if axes.get("procedure", 0) > 0.6 or reasoning_type == "procedural":
            return self._summarize_procedure(article)

        # -----------------------------
        # 3. concept（概念中心）
        # -----------------------------
        if axes.get("concept", 0) > 0.6 or reasoning_type == "conceptual":
            return self._summarize_concept(article)

        # -----------------------------
        # 4. example（例中心）
        # -----------------------------
        if axes.get("example", 0) > 0.6:
            return self._summarize_example(article)

        # -----------------------------
        # 5. explain（説明中心）
        # -----------------------------
        if axes.get("explain", 0) > 0.6:
            return self._summarize_explain(article)

        # -----------------------------
        # 6. notes（注意点中心）
        # -----------------------------
        if axes.get("notes", 0) > 0.6:
            return self._summarize_notes(article)

        # -----------------------------
        # 7. fallback（構造化要約）
        # -----------------------------
        return self._summarize_structure(article)

    # =========================================================
    # 各要約スタイルの実装
    # =========================================================

    def _summarize_structure(self, article):
        lines = article.split("\n")
        summary = ["# 構造化要約"]

        for line in lines:
            if line.strip().startswith(("#", "##", "###")):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])

    def _summarize_procedure(self, article):
        lines = article.split("\n")
        summary = ["# 手順中心の要約"]

        for line in lines:
            if re.search(r"(Step|手順|まず|次に|最後に)", line):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])

    def _summarize_concept(self, article):
        lines = article.split("\n")
        summary = ["# 概念中心の要約"]

        for line in lines:
            if re.search(r"(とは|定義|概念|ポイント)", line):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])

    def _summarize_example(self, article):
        lines = article.split("\n")
        summary = ["# 例中心の要約"]

        for line in lines:
            if re.search(r"(例|ケース|サンプル)", line):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])

    def _summarize_explain(self, article):
        lines = article.split("\n")
        summary = ["# 説明中心の要約"]

        for line in lines:
            if re.search(r"(理由|なぜ|because|説明)", line):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])

    def _summarize_notes(self, article):
        lines = article.split("\n")
        summary = ["# 注意点中心の要約"]

        for line in lines:
            if re.search(r"(注意|警告|危険|重要)", line):
                summary.append(f"- {line.strip()}")

        return "\n".join(summary[:12])
