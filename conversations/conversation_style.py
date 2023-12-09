from enum import Enum


class ConversationStyle(Enum):
    PRECISE: str = "precise"
    BALANCED: str = "balanced"
    CREATIVE: str = "creative"
    PRECISE_OFFLINE: str = "precise-offline"
    BALANCED_OFFLINE: str = "balanced-offline"
    CREATIVE_OFFLINE: str = "creative-offline"
