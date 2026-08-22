# ============================================================
# KeywordStrength（強化版：cosine + keyword weight + decay）
# ============================================================

def keyword_strength(tokens, embed, direction, keyword_dict=None):
    # 1. cosine 類似度（元の構造）
    vecs = [embed(t) for t in tokens]
    score = sum(cosine(v, direction) for v in vecs)

    # 2. キーワード重み付け（強化）
    if keyword_dict:
        for strength, words in keyword_dict.items():
            weight = {"strong": 1.0, "medium": 0.7, "weak": 0.4}[strength]
            for w in words:
                if w in tokens:
                    score += weight

    # 3. 長文減衰（強化）
    score /= (len(tokens) ** 0.5 + 1e-9)

    return score
