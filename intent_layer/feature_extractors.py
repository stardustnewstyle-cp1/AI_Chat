# intent_layer/feature_extractor.py

import re

def tokenize(text: str):
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z]+|[ぁ-んァ-ン一-龥]+", text)
    return tokens

def extract_features(text: str, feature_groups):
    tokens = tokenize(text)
    detected = {axis: [] for axis in feature_groups.keys()}

    for axis, groups in feature_groups.items():
        for subcategory, words in groups.items():
            for w in words:
                if w in text:
                    detected[axis].append((subcategory, w))

    return detected
