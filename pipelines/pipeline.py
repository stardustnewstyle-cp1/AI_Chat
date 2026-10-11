class Pipeline:

    def __init__(self):
        self.intent_detector = IntentDetector()
        self.technical_reasoner = TechnicalReasoner()
        self.api_router = APIRouter()
        self.reasoning_layer = ReasoningLayer()

    def run_pipeline(self, user_input):

        # 1. Intent
        intent_result = self.intent_detector.run(user_input)
        score = intent_result["score"]

        # 2. TechnicalReasoner
        tech_result = self.technical_reasoner.run(user_input, score)

        # 3. Router
        router_result = self.api_router.run(user_input)

        # 4. ReasoningLayer
        reasoning_result = self.reasoning_layer.run(
            text=user_input,
            api_info=router_result,
            reasoning_type=tech_result["reasoning_type"],
            features=tech_result["features"]
        )

        return {
            "intent_result": intent_result,
            "tech_result": tech_result,
            "router_result": router_result,
            "reasoning_result": reasoning_result
        }
