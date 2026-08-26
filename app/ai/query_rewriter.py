from langchain_mistralai import ChatMistralAI

from app.core.config import settings


class QueryRewriter:

    @staticmethod
    def rewrite(
        question: str,
        history: list
    ):

        # ----------------------------------------
        # No previous conversation
        # ----------------------------------------

        if not history:
            return question


        # ----------------------------------------
        # Build conversation text
        # ----------------------------------------

        conversation = ""

        for message in history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            conversation += (
                f"{role.upper()}: {content}\n"
            )


        # ----------------------------------------
        # LLM
        # ----------------------------------------

        llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0,
            api_key=settings.MISTRAL_API_KEY
        )


        prompt = f"""
You are the query rewriting component of
DineEase, a restaurant chatbot.

Your ONLY job is to convert the latest user
question into a standalone question that can
be searched against a restaurant menu and
restaurant policy knowledge base.

DO NOT answer the question.

DO NOT add information that is not present
in the conversation.

========================================
CONVERSATION HISTORY
========================================

{conversation}

========================================
LATEST USER QUESTION
========================================

{question}

========================================
REWRITING RULES
========================================


1. Resolve references to a specific entity.

Example:

Previous:
USER: Tell me about Farmhouse Pizza.

Latest:
USER: How much does it cost?

Output:
What is the price of Farmhouse Pizza?


2. Preserve collection references.

If the previous answer contains multiple items,
and the user asks:

- Which one
- Which ones
- Which is vegetarian
- Which are vegetarian
- Which is cheapest
- Which are spicy
- Which one is available
- Which ones are available

DO NOT reduce the question to the first item.

Instead, preserve the collection.

Example:

Previous:
USER: What pizzas do you have?

ASSISTANT:
We have Farmhouse Pizza and Cheese Burst Pizza.

Latest:
USER: Which one is vegetarian?

Output:
Which of the available pizzas are vegetarian?


Example:

Previous:
USER: What pizzas do you have?

ASSISTANT:
We have Farmhouse Pizza and Cheese Burst Pizza.

Latest:
USER: Which one is cheapest?

Output:
Which of the available pizzas is the cheapest?


Example:

Previous:
USER: What paneer dishes do you have?

ASSISTANT:
We have Paneer Kadhai, Palak Paneer and Paneer Tikka Masala.

Latest:
USER: Which ones are spicy?

Output:
Which of the available paneer dishes are spicy?


3. Resolve references such as:

- it
- this
- that
- this dish
- this pizza
- this item
- the dish
- the pizza
- the item

when the conversation clearly refers to ONE specific item.


4. If the conversation refers to MULTIPLE items,
preserve the group instead of selecting only one.


5. If the latest question is already standalone,
return it unchanged.


6. Preserve the user's actual intent.


7. Never answer the question.


8. Never invent menu items.


9. Return ONLY the rewritten standalone question.

========================================
REWRITTEN QUESTION
========================================
"""

        response = llm.invoke(
            prompt
        )

        rewritten_question = (
            response.content
            .strip()
        )

        return rewritten_question