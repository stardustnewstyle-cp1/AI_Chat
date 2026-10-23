# pipeline/pipeline.py
# ============================================================
# 技術特化 AI：IntentDetector → ReasoningLayer → ML → TeacherLayer → LLM
# ============================================================

from intent_layer.intent_detector import IntentDetector
from reasoning_layer.reasoning_layer import ReasoningLayer
from teacher_layer.teacher_layer import TeacherLayer
from ml.feature_extractor import FeatureExtractor
from ml.level_detector import LevelDetector

class Pipeline:
    def __init__(self, llm):
        """
        llm: 実際の LLM（OpenAI / Azure / 自作モデルなど）
        """
        self.llm = llm

        # 新構造の各層
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()

        # ML（骨格）
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    def run(self, text: str):
        """
        技術特化 AI の最短ルート Pipeline
        Intent → Reasoning → ML → Teacher → LLM
        """

        # ---------------------------------------------------------
        # 1. IntentDetector（意味理解）
        # ---------------------------------------------------------
        intent_result = self.intent_detector.detect(text)
        domain = intent_result["domain"]

        # ---------------------------------------------------------
        # ★ 非技術質問ならここで止める（重要）
        # ---------------------------------------------------------
        if domain == "non_technical":
            return {
                "title": "非技術質問",
                "sections": [
                    {
                        "header": "このAIは技術専用です",
                        "content": "技術に関係ない質問には回答できません。プログラミング・AI・開発・設計などの技術的な内容を入力してください。"
                    }
                ]
            }

        # ---------------------------------------------------------
        # 2. ReasoningLayer（推論タイプ決定）
        # ---------------------------------------------------------
        intent = intent_result.get("intent")
        axes = intent_result.get("axes")
        score = intent_result.get("score")

        reasoning_type = self.reasoning_layer.run(
            domain=domain,
            intent=intent,
            axes=axes
        )

        # ---------------------------------------------------------
        # 3. ML（特徴量抽出 → レベル判定）
        # ---------------------------------------------------------
        features = self.extractor.extract(text)
        level = self.level_detector.detect(features)

        # ---------------------------------------------------------
        # 4. TeacherLayer（構造化）
        # ---------------------------------------------------------
        teacher_output = self.teacher_layer.run(
            text=text,
            domain=domain,
            intent=intent,
            reasoning_type=reasoning_type,
            level=level,
            axes=axes
        )

        # ---------------------------------------------------------
        # 5. LLM（文章化）
        # ---------------------------------------------------------
        llm_output = self.llm.generate(teacher_output)

        # ---------------------------------------------------------
        # 6. 統合結果
        # ---------------------------------------------------------
        return {
            "intent": intent_result,
            "reasoning_type": reasoning_type,
            "features": features,
            "level": level,
            "teacher_output": teacher_output,
            "llm_output": llm_output
        }
