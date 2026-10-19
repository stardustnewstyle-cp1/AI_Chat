# pipeline/pipeline.py
# ============================================================
# 技術特化 AI：IntentDetector → ReasoningLayer → ML → TeacherLayer → LLM
# ============================================================

from intent_layer.intent_detector import IntentDetector
from reasoning_layer.reasoning_layer import ReasoningLayer
from teacher_layer.teacher_layer import TeacherLayer

from ml.feature_extraction import FeatureExtractor
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

        # 1. IntentDetector（意味理解）
        intent_result = self.intent_detector.run(text)

        domain = intent_result["domain"]
        intent = intent_result["intent"]
        axes = intent_result["axes"]
        score = intent_result["score"]

        # 2. ReasoningLayer（推論タイプ決定）
        reasoning_type = self.reasoning_layer.run(
            domain=domain,
            intent=intent,
            axes=axes
        )

        # 3. ML（特徴量抽出 → レベル判定）
        features = self.extractor.extract(text)
        level = self.level_detector.detect(features)

        # 4. TeacherLayer（構造化）
        teacher_output = self.teacher_layer.run(
            text=text,
            domain=domain,
            intent=intent,
            reasoning_type=reasoning_type,
            level=level,
            axes=axes
        )

        # 5. LLM（文章化）
        llm_output = self.llm.generate(teacher_output)

        # 6. 統合結果
        return {
            "intent": intent_result,
            "reasoning_type": reasoning_type,
            "features": features,
            "level": level,
            "teacher_output": teacher_output,
            "llm_output": llm_output
        }
