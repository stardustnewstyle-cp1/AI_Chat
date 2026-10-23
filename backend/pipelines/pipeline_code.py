# pipeline/pipeline_code.py
# ============================================================
# 技術コード生成：IntentDetector → ReasoningLayer → TeacherLayer → CodeGenerator → LLM
# ============================================================

from intent_layer.intent_detector import IntentDetector
from reasoning_layer.reasoning_layer import ReasoningLayer
from teacher_layer.teacher_layer import TeacherLayer


class CodePipeline:
    def __init__(self, llm):
        """
        llm: 実際の LLM（OpenAI / Azure / 自作モデルなど）
        """
        self.llm = llm

        
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        

    def run(self, text: str, api_info: dict):
        """
        技術コード生成専用パイプライン
        Intent → Reasoning → Teacher → CodeGenerator → LLM
        """

        # 1. IntentDetector（意味理解）
        intent_result = self.intent_detector.run(text)

        domain = intent_result["domain"]
        intent = intent_result["intent"]
        axes = intent_result["axes"]

        # 2. ReasoningLayer（推論タイプ決定）
        reasoning_type = self.reasoning_layer.run(
            domain=domain,
            intent=intent,
            axes=axes
        )

        # 3. TeacherLayer（構造化）
        teacher_output = self.teacher_layer.run(
            text=text,
            domain=domain,
            intent=intent,
            reasoning_type=reasoning_type,
            level=None,   # コード生成では ML レベル不要
            axes=axes
        )

        # 4. CodeGenerator（API 情報を使ったコード生成）
        code_output = self.code_generator.run(
            api_info=api_info,
            teacher_output=teacher_output,
            intent=intent,
            reasoning_type=reasoning_type
        )

        # 5. LLM（最終文章化）
        llm_output = self.llm.generate(code_output)

        # 6. 統合結果
        return {
            "intent": intent_result,
            "reasoning_type": reasoning_type,
            "teacher_output": teacher_output,
            "code_output": code_output,
            "llm_output": llm_output
        }
