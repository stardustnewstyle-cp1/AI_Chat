# pipelines/pipeline.py

from backend.intent_layer.intent_detector import IntentDetector
from backend.reasoning_layer.reasoning_layer import ReasoningLayer
from backend.teacher_layer.teacher_layer import TeacherLayer
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.level_detector import LevelDetector
from backend.llm.llm import LLM


class Pipeline:
    def __init__(self, llm: LLM):
        self.llm = llm
        self.intent_detector = IntentDetector()
        self.reasoning_layer = ReasoningLayer()
        self.teacher_layer = TeacherLayer()
        self.extractor = FeatureExtractor()
        self.level_detector = LevelDetector()

    def run(self, text: str):

        # 1. IntentDetector
        intent_result = self.intent_detector.detect(text)
        domain = intent_result["domain"]

        # 非技術質問
        if domain == "non_technical":
            return {
                "title": "非技術質問",
                "sections": [
                    {
                        "header": "このAIは技術専用です",
                        "content": "技術に関係ない質問には回答できません。"
                    }
                ]
            }

        # 2. ReasoningLayer
        intent = intent_result.get("intent")
        axes = intent_result.get("axes")
        score = intent_result.get("score")

        reasoning_type = self.reasoning_layer.map_domain_to_reasoning(domain)

        # 3. ML
        features = self.extractor.extract(text)
        level = self.level_detector.detect(features)

        # 4. TeacherLayer
        sections = self.teacher_layer.run({
            "domain": domain,
            "intent": intent,
            "reasoning_type": reasoning_type,
            "level": level,
            "axes": axes,
            "score": score,
            "title": "回答"
        })["sections"]

        # 5. UI 用レスポンス
        return {
            "intent": intent,
            "reasoning": reasoning_type,
            "level": level,
            "score": score,
            "sections": sections
        }
