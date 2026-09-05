def compute_ambiguity(axis_scores, keyword_density, context_match):
    import numpy as np

    max_axis = max(axis_scores.values())
    variance = np.var(list(axis_scores.values()))

    w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1

    ambiguity_score = (
        (1 - max_axis) * w1 +
        variance * w2 +
        (1 - keyword_density) * w3 +
        (1 - context_match) * w4
    )

    return ambiguity_score
