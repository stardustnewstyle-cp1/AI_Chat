# intent_layer/intent_selector.py

def select_intent(scores):
    max_score = max(scores.values())
    if max_score == 0:
        return "unknown"

    intents = [axis for axis, score in scores.items() if score == max_score]

    if len(intents) == 1:
        return intents[0]

    return intents  # 複合意図
