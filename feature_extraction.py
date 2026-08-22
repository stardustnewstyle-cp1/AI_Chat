import re

class FeatureExtractor:
    LOGIC_CONNECTIVES = ["しかし", "つまり", "一方で", "なぜなら", "だから", "そのため"]
    TECH_KEYWORDS = ["CPU", "メモリ", "AI", "モデル", "推論", "クラウド", "アルゴリズム"]

    def extract(self, text):
        features = {}

        features["connectives"] = self._count_connectives(text)
        features["structure_score"] = self._structure_score(text)
        features["causal_links"] = self._count_causal_links(text)
        features["concept_density"] = self._concept_density(text)
        features["generalization_level"] = self._generalization_level(text)
        features["tech_terms"] = self._count_tech_terms(text)
        features["domain_specificity"] = self._domain_specificity(text)
        features["intent_clarity"] = self._intent_clarity(text)
        features["goal_alignment"] = self._goal_alignment(text)
        features["section_flow"] = self._section_flow(text)
        features["hierarchy_depth"] = self._hierarchy_depth(text)

        return features

    def _count_connectives(self, text):
        return sum(text.count(c) for c in self.LOGIC_CONNECTIVES)

    def _structure_score(self, text):
        sections = text.split("\n")
        return min(len(sections), 10) / 10

    def _count_causal_links(self, text):
        causal_words = ["理由", "原因", "結果", "影響"]
        return sum(text.count(w) for w in causal_words)

    def _concept_density(self, text):
        words = text.split()
        return len(set(words)) / max(len(words), 1)

    def _generalization_level(self, text):
        abstract_words = ["概念", "抽象", "一般化", "構造"]
        return sum(text.count(w) for w in abstract_words)

    def _count_tech_terms(self, text):
        return sum(text.count(t) for t in self.TECH_KEYWORDS)

    def _domain_specificity(self, text):
        return self._count_tech_terms(text) / 10

    def _intent_clarity(self, text):
        return 1.0 if "目的" in text or "意図" in text else 0.3

    def _goal_alignment(self, text):
        return 1.0 if "達成" in text or "ゴール" in text else 0.4

    def _section_flow(self, text):
        return 0.8 if "\n" in text else 0.3

    def _hierarchy_depth(self, text):
        return text.count("・") + text.count("-")
