def extract_features(self, text, source_bias):
    """
    Intent Layer の特徴量抽出。
    """

    # ① KeywordStrength：キーワードの出現頻度
    keyword_strength = sum(
        kw in text for kw in KEYWORDS
    )

    # ② ContextStrength：文章の目的性（疑問・依頼・説明）
    context_strength = (
        1 if "?" in text else
        2 if "教えて" in text or "方法" in text else
        0
    )

    # ③ StructureStrength：文章の構造的手がかり
    structure_strength = (
        text.count("・") +
        text.count("→") +
        text.count("①") +
        text.count("1.")
    )

    # ④ SourceStrength：入力元の信頼性（bias）
    source_strength = source_bias

    return {
        "keyword_strength": keyword_strength,
        "context_strength": context_strength,
        "structure_strength": structure_strength,
        "source_strength": source_strength,
    }
