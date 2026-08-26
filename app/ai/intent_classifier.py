from enum import Enum


class ChatIntent(str, Enum):

    MENU = "menu"
    POLICY = "policy"
    GENERAL = "general"


def classify_intent(question: str) -> ChatIntent:

    text = question.lower().strip()

    # =================================
    # POLICY
    # =================================

    policy_keywords = [
        "policy",
        "policies",
        "cancel",
        "cancellation",
        "refund",
        "money back",
        "reservation charge",
        "reservation fee",
        "booking charge",
        "booking fee",
        "cancellation window",
        "cancel my reservation",
        "cancel reservation",
        "reservation rules",
        "booking rules",
        "food bill threshold",
        "food cutoff",
        "add food",
        "add items",
        "reservation payment",
        "booking payment"
    ]

    if any(
        keyword in text
        for keyword in policy_keywords
    ):
        return ChatIntent.POLICY


    # =================================
    # MENU
    # =================================

    menu_keywords = [
        "menu",
        "dish",
        "food",
        "paneer",
        "pizza",
        "biryani",
        "dessert",
        "drink",
        "starter",
        "soup",
        "salad",
        "bread",
        "rice",
        "noodles",
        "vegetarian",
        "vegetarian",
        "veg",
        "non veg",
        "non-veg",
        "price",
        "cost",
        "available",
        "availability",
        "calories",
        "spicy",
        "spice",
        "rating",
        "preparation time",
        "ingredients",
        "contains",
        "recommend"
    ]

    if any(
        keyword in text
        for keyword in menu_keywords
    ):
        return ChatIntent.MENU


    # =================================
    # GENERAL
    # =================================

    return ChatIntent.GENERAL