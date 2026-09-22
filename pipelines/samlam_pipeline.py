# ============================================
# SAMLRM_Pipeline.py 
# ============================================

from intent_layer.intent_layer import intent_layer
from reasoning_layer.reasoning_layer import ReasoningLayer
from teacher_layer.teacher_layer import TeacherLayer
from router.intent_reasoning_router import IntentReasoningRouter

class Pipeline:

    def __init__(self, llm):
        """
        llm: 実際の LLM（OpenAI / Azure / 自作モデルなど）
        """
        self.llm = llm
        self.router = IntentReasoningRouter()

    def run(self, user_input, api_info=None):
        """
        SAMLRM の全層を統合して実行する。
        """

        # ----------------------------------------
        # 1. Router（Intent → Reasoning → Code → Teacher）
        # ----------------------------------------
        router_result = self.router.handle(user_input, api_info)

        # ----------------------------------------
        # 2. LLM に渡す文章を作る
        # ----------------------------------------
        if router_result["mode"] == "technical_code":
            final_text = router_result["final_output"]

        elif router_result["mode"] == "technical_explain":
            final_text = router_result["final_output"]

        else:
            # 非技術質問
            final_text = router_result["message"]

        # ----------------------------------------
        # 3. LLM による文章化
        # ----------------------------------------
        llm_output = self.llm.generate(final_text)

        # ----------------------------------------
        # 4. 最終結果を返す
        # ----------------------------------------
        return {
            "router": router_result,
            "llm_output": llm_output
        }
