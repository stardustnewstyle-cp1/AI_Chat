# ============================================
# teacher_layer.py — SAMLRM Teacher Layer
# ============================================

class TeacherLayer:

    def generate_expected_output(self, intent_result, raw_output):
        """
        理想回答（expected_output）を生成する。
        intent_result と raw_output を見て、
        「本来こうあるべき」という形を作る。
        """

        reasoning_type = intent_result["reasoning_type"]
        axes_tech = intent_result.get("axes_tech", {})

        expected = []

        # -----------------------------
        # 1. 技術質問なら構造を整える
        # -----------------------------
        if intent_result["technical"]:
            expected.append("# 技術回答（理想形）")

            # コードが必要
            if axes_tech.get("code", 0) > 0.5:
                expected.append("# コードを含めるべき")

            # 例が必要
            if axes_tech.get("example", 0) > 0.5:
                expected.append("# 例を含めるべき")

            # 説明が必要
            if axes_tech.get("explain", 0) > 0.5:
                expected.append("# 説明を含めるべき")

            # 注意点が必要
            if axes_tech.get("notes", 0) > 0.5:
                expected.append("# 注意点を含めるべき")

            # 設計が必要
            if axes_tech.get("design", 0) > 0.5:
                expected.append("# 設計情報を含めるべき")

        else:
            expected.append("一般回答（理想形）")
            expected.append("・簡潔に説明する")
            expected.append("・構造化する")

        return "\n".join(expected)

    # ---------------------------------------------------------
    # 差分検出
    # ---------------------------------------------------------
    def compare(self, expected_output, raw_output):
        """
        expected_output と raw_output の差分を検出する。
        """
        expected_lines = expected_output.split("\n")
        raw_lines = raw_output.split("\n")

        missing = []

        for line in expected_lines:
            if line.startswith("#") and line not in raw_lines:
                missing.append(line)

        return missing

    # ---------------------------------------------------------
    # 改善適用
    # ---------------------------------------------------------
    def apply_improvement(self, raw_output, missing_items):
        """
        差分（missing_items）を raw_output に追加して改善する。
        """
        improved = raw_output.split("\n")

        if missing_items:
            improved.append("\n# --- Teacher Layer による改善 ---")
            for m in missing_items:
                improved.append(m)

        return "\n".join(improved)

    # ---------------------------------------------------------
    # Teacher Layer の統合処理
    # ---------------------------------------------------------
    def improve(self, intent_result, raw_output):
        """
        Teacher Layer の全処理をまとめた関数。
        """
        expected = self.generate_expected_output(intent_result, raw_output)
        missing = self.compare(expected, raw_output)
        improved = self.apply_improvement(raw_output, missing)

        return {
            "expected_output": expected,
            "missing_items": missing,
            "final_output": improved
        }
