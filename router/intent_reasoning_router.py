# ============================================
# intent_reasoning_router.py
# SAMLRM — Intent → Reasoning → Code → Teacher Router
# ============================================

from intent_layer.intent_layer import intent_layer
from reasoning_layer.reasoning_layer import ReasoningLayer
from teacher_layer.teacher_layer import TeacherLayer

class IntentReasoningRouter:

    def __init__(self):
        self.reasoning = ReasoningLayer()
        self.teacher = TeacherLayer()

    def handle(self, user_input, api_info=None):
        """
        user_input: ユーザー入力
        api_info: API情報（コード生成が必要な場合）
        """

        # -----------------------------
        # 1. Intent Layer（意味解析）
        # -----------------------------
        intent_result = intent_layer(user_input)

        # 技術質問かどうか
        technical = intent_result["technical"]

        # -----------------------------
        # 2. 非技術質問ならここで終了
        # -----------------------------
        if not technical:
            return {
                "mode": "general",
                "message": "これは技術質問ではありません。",
                "intent_result": intent_result
            }

        # -----------------------------
        # 3. Reasoning Layer（方針生成）
        # -----------------------------
        reasoning_type = intent_result["reasoning_type"]
        intent_type = self.reasoning.select_code_intent(reasoning_type)

        # -----------------------------
        # 4. コード生成が必要か？
        # -----------------------------
        if api_info is not None:
            raw_output = self.reasoning.generate_code(api_info, intent_type)

            # -----------------------------
            # 5. Teacher Layer（改善）
            # -----------------------------
            improved = self.teacher.improve(intent_result, raw_output)

            return {
                "mode": "technical_code",
                "intent_type": intent_type,
                "raw_output": raw_output,
                "final_output": improved["final_output"],
                "missing_items": improved["missing_items"],
                "expected_output": improved["expected_output"],
                "intent_result": intent_result
            }

        # -----------------------------
        # 6. コード生成なし → 技術説明モード
        # -----------------------------
        raw_output = f"技術質問です。方針: {intent_type}"

        improved = self.teacher.improve(intent_result, raw_output)

        return {
            "mode": "technical_explain",
            "intent_type": intent_type,
            "raw_output": raw_output,
            "final_output": improved["final_output"],
            "missing_items": improved["missing_items"],
            "expected_output": improved["expected_output"],
            "intent_result": intent_result
        }
