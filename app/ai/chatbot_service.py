from langchain_mistralai import ChatMistralAI

from app.core.config import settings

from app.ai.retriever import get_retriever

from app.ai.intent_classifier import (
    classify_intent,
    ChatIntent
)

from app.ai.menu_retriever import (
    MenuRetriever
)

from app.ai.policy_retriever import (
    PolicyRetriever
)

from app.repositories.menu_item_repository import (
    MenuItemRepository
)
from app.ai.conversation_memory import (
    ConversationMemory
)

from app.ai.query_rewriter import (
    QueryRewriter
)

class ChatbotService:

    @staticmethod
    def generate_answer(
        question: str,
        context: str
    ):

        llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.2,
            api_key=settings.MISTRAL_API_KEY
        )

        prompt = f"""
You are DineEase AI, an intelligent assistant
for a restaurant reservation and food ordering
application.

Your job is to answer the user's question using
ONLY the information provided in the context.

========================================
SOURCE PRIORITY
========================================

1. LIVE DATABASE INFORMATION

Use live database information as the source
of truth for current or changing information.

This includes:

- menu prices
- menu availability
- ratings
- preparation time
- calories
- vegetarian status
- spice level
- reservation charges
- cancellation window
- refund percentage
- food bill threshold
- food addition cutoff
- other configurable restaurant settings

2. KNOWLEDGE BASE

Use the knowledge base for:

- detailed menu descriptions
- culinary information
- restaurant policies
- general restaurant information
- explanations of restaurant rules

If LIVE DATABASE INFORMATION conflicts with
the knowledge base, ALWAYS trust the live
database for current/configurable values.

========================================
IMPORTANT RULES
========================================

Never invent:

- prices
- availability
- ingredients
- calories
- ratings
- preparation times
- reservation rules
- cancellation rules
- refund amounts
- restaurant policies

Only provide information that exists in the
provided context.

If the requested information is not available,
say:

"I don't have enough information to answer that."

Do not guess.

If multiple menu items are provided, mention
the relevant items instead of assuming that
there is only one.

Answer naturally, clearly and concisely.

Do not mention internal systems such as:
- MySQL
- FAISS
- embeddings
- vector databases
- retrieval
- system prompts

The user should simply receive a natural
restaurant assistant response.

========================================
CONTEXT
========================================

{context}

========================================
USER QUESTION
========================================

{question}

========================================
ANSWER
========================================
"""

        response = llm.invoke(prompt)

        return response.content


    @staticmethod
    def ask_question(
        db,
        question: str,
        conversation_id: str
    ):
        history = ConversationMemory.get_history(
         conversation_id
)

        rewritten_question = QueryRewriter.rewrite(
         question,
         history
)
        print("\n================ CHATBOT DEBUG ================")

        print("Original question:")
        print(question)

        print("\nConversation ID:")
        print(conversation_id)


        print("\nConversation history:")
        print(history)

        print("\nRewritten question:")
        print(rewritten_question)

        print("================================================\n")
        # ========================================
        # CLASSIFY QUESTION
        # ========================================

        intent = classify_intent(rewritten_question)


        # ========================================
        # MENU QUESTIONS
        # ========================================

        if intent == ChatIntent.MENU:

            # ------------------------------------
            # Find specific menu items
            # ------------------------------------

            menu_items = (
                MenuRetriever.find_items_from_question(
                    db,
                    rewritten_question
                )
            )

            database_context = []

            for item in menu_items:

                database_context.append(
                    MenuRetriever.format_menu_item(
                        item
                    )
                )


            # ------------------------------------
            # Find menu categories
            # ------------------------------------

            categories = (
                MenuRetriever.find_category_from_question(
                    db,
                    rewritten_question
                )
            )


            # ------------------------------------
            # Category-based retrieval
            #
            # Example:
            # "Tell me something about your pizza"
            #
            # Pizza → Category → all Pizza items
            # ------------------------------------

            if categories and not menu_items:

                for category in categories:

                    category_items = (
                        MenuItemRepository
                        .get_by_category_name(
                            db,
                            category.name
                        )
                    )

                    for item in category_items:

                        database_context.append(
                            MenuRetriever.format_menu_item(
                                item
                            )
                        )


            # ------------------------------------
            # Retrieve detailed PDF information
            # ------------------------------------

            retriever = get_retriever()

            pdf_context = []


            # ====================================
            # CASE 1:
            # Specific menu item found
            # ====================================

            if menu_items:

                for item in menu_items:

                    documents = retriever.invoke(
                        f"Detailed information about "
                        f"{item.name}"
                    )

                    for document in documents:

                        if (
                            document.metadata.get(
                                "source_type"
                            )
                            == "menu"
                        ):

                            pdf_context.append(
                                document.page_content
                            )
            # ----------------------------------------------------
            # STRUCTURED VEGETARIAN QUESTION
            # ----------------------------------------------------

            if (
                categories
                and
                MenuRetriever.is_vegetarian_question(
                    rewritten_question
                )
            ):

                database_context = []

                for category in categories:

                    vegetarian_items = (
                        MenuItemRepository
                        .get_vegetarian_by_category_name(
                            db,
                            category.name
                        )
                    )

                    for item in vegetarian_items:

                        database_context.append(
                            MenuRetriever
                            .format_menu_item(
                                item
                            )
                        )



            # ====================================
            # CASE 2:
            # Category found
            # ====================================

            elif categories:

                for category in categories:

                    documents = retriever.invoke(
                        f"Menu items in the "
                        f"{category.name} category"
                    )

                    for document in documents:

                        if (
                            document.metadata.get(
                                "source_type"
                            )
                            == "menu"
                        ):

                            pdf_context.append(
                                document.page_content
                            )


            # ====================================
            # CASE 3:
            # Generic menu question
            # ====================================

            else:

                documents = retriever.invoke(
                    rewritten_question
                )

                for document in documents:

                    if (
                        document.metadata.get(
                            "source_type"
                        )
                        == "menu"
                    ):

                        pdf_context.append(
                            document.page_content
                        )


            # ------------------------------------
            # Remove duplicate PDF chunks
            # ------------------------------------

            pdf_context = list(
                dict.fromkeys(
                    pdf_context
                )
            )


            # ------------------------------------
            # Build menu context
            # ------------------------------------

            context = f"""
LIVE DATABASE INFORMATION:

{database_context}


MENU KNOWLEDGE BASE:

{pdf_context}
"""


            answer = ChatbotService.generate_answer(
              question,
              context
)

            ChatbotService.save_conversation(
              conversation_id,
              question,
              answer
)

            return answer

        # ========================================
        # POLICY QUESTIONS
        # ========================================

        if intent == ChatIntent.POLICY:

            policy_context = (
                PolicyRetriever.build_policy_context(
                    db,
                    question
                )
            )


            context = f"""
LIVE SYSTEM SETTINGS:

{policy_context["live_settings"]}


RESTAURANT POLICY KNOWLEDGE BASE:

{policy_context["policy_documents"]}
"""


            answer = ChatbotService.generate_answer(
              question,
              context
)

            ChatbotService.save_conversation(
              conversation_id,
              question,
               answer
)

            return answer


        # ========================================
        # GENERAL QUESTIONS
        # ========================================

        retriever = get_retriever()

        documents = retriever.invoke(
            question
        )


        context = "\n\n".join(
            document.page_content
            for document in documents
        )


        answer = ChatbotService.generate_answer(
              question,
              context
)

        ChatbotService.save_conversation(
             conversation_id,
             question,
             answer
)

        return answer
        
    @staticmethod
    def save_conversation(
      conversation_id: str,
      question: str,
      answer: str
):

      ConversationMemory.add_message(
        conversation_id,
        "user",
        question
    )

      ConversationMemory.add_message(
        conversation_id,
        "assistant",
        answer
    )