# intent_layer/feature_loader.py

from feature_groups.structure_features import STRUCTURE_FEATURES
from feature_groups.concept_features import CONCEPT_FEATURES
from feature_groups.causality_features import CAUSALITY_FEATURES
from feature_groups.improvement_features import IMPROVEMENT_FEATURES
from feature_groups.abstraction_features import ABSTRACTION_FEATURES
from feature_groups.organization_features import ORGANIZATION_FEATURES
from feature_groups.contrast_features import CONTRAST_FEATURES
from feature_groups.selection_features import SELECTION_FEATURES
from feature_groups.representation_features import REPRESENTATION_FEATURES
from feature_groups.emotion_features import EMOTION_FEATURES

FEATURE_GROUPS = {
    "structure": STRUCTURE_FEATURES,
    "concept": CONCEPT_FEATURES,
    "causality": CAUSALITY_FEATURES,
    "improvement": IMPROVEMENT_FEATURES,
    "abstraction": ABSTRACTION_FEATURES,
    "organization": ORGANIZATION_FEATURES,
    "contrast": CONTRAST_FEATURES,
    "selection": SELECTION_FEATURES,
    "representation": REPRESENTATION_FEATURES,
    "emotion": EMOTION_FEATURES
}
