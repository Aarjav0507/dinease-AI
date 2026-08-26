from sqlalchemy.orm import Session

from app.services.system_settings_service import (
    SystemSettingsService
)

from app.ai.retriever import get_retriever


class PolicyRetriever:

    @staticmethod
    def get_live_settings(
        db: Session
    ):

        settings = (
            SystemSettingsService.get_settings(
                db
            )
        )

        return {
            "reservation_charge_per_hour_per_guest":
                settings.reservation_charge_per_hour_per_guest,

            "cancellation_window_hours":
                settings.cancellation_window_hours,

            "refund_percentage":
                settings.refund_percentage,

            "food_bill_threshold":
                settings.food_bill_threshold,

            "food_addition_cutoff_minutes":
                settings.food_addition_cutoff_minutes
        }

    @staticmethod
    def get_policy_documents(
        question: str
    ):

        retriever = get_retriever()

        documents = retriever.invoke(
            question
        )

        policy_documents = [
            document
            for document in documents
            if document.metadata.get(
                "source_type"
            ) == "policy"
        ]

        return policy_documents

    @staticmethod
    def build_policy_context(
        db: Session,
        question: str
    ):

        # Live database settings
        settings = (
            PolicyRetriever.get_live_settings(
                db
            )
        )

        # Detailed policy PDF
        documents = (
            PolicyRetriever.get_policy_documents(
                question
            )
        )

        policy_information = []

        for document in documents:

            policy_information.append(
                document.page_content
            )

        return {
            "live_settings": settings,
            "policy_documents": policy_information
        }