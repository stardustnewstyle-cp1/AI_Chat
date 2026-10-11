#reasoning_pipeline.py
##----------------------------------------
##意図抽出のために、推論層（TechnicalReasoner）を接続する
##----------------------------------------
from intent_layer.intent_detector import IntentDetector
from reasoning_layer.technical_reasoning import TechnicalReasoner
from reasoning_layer.reasoning_layer import ReasoningLayer

class ReasoningPipeline:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.technical_reasoner = TechnicalReasoner()
        self.reasoning_layer = ReasoningLayer()

    def run(self, text):
        #1.Intent Detection
        intent, score = self.intent_detector.classify_intent(text)
        #2. Technical Reasoning
        features = self.technical_reasoning.extract_features(text, source_bias=score)

        reasoning_result = self.technical_reasoning.classify_reasoning_type(features)
        #3. Reasoning_Layer
        reasoning_output = self.reasoning_layer.run(text, api_info=None, reasoning_type=reasoning_result, features)
        return {
            "intent": intent,
            "score": score,
            "features": features,
            "reasoning_result": reasoning_result,
            "reasoning_output": reasoning_output
        }

         

    