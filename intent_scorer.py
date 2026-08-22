# intent_layer/intent_scorer.py

def score_intent(detected_features):
    scores = {}

    for axis, items in detected_features.items():
        score = 0
        for subcategory, word in items:
            score += 1  # 後で重み付け可能
        scores[axis] = score

    return scores
