from sqlalchemy.orm import Session

from app.repositories.menu_item_repository import (
    MenuItemRepository
)

from app.ai.retriever import get_retriever


class MenuRetriever:

    @staticmethod
    def search_menu_item(
        db: Session,
        name: str
    ):
        return MenuItemRepository.search_by_name(
            db,
            name
        )

    @staticmethod
    def format_menu_item(
        menu_item
    ):

        category_name = (
            menu_item.category.name
            if menu_item.category
            else "Unknown"
        )

        return {
            "id": menu_item.id,
            "name": menu_item.name,
            "category": category_name,
            "description": menu_item.description,
            "price": float(menu_item.price),
            "preparation_time": menu_item.preparation_time,
            "calories": menu_item.calories,
            "spice_level": menu_item.spice_level,
            "rating": float(menu_item.rating),
            "is_veg": menu_item.is_veg,
            "is_available": menu_item.is_available
        }

    @staticmethod
    def get_detailed_information(
      item_name: str
):

      retriever = get_retriever()

      documents = retriever.invoke(
        f"Detailed information about {item_name}"
    )

      menu_documents = [
        document
        for document in documents
        if document.metadata.get("source_type")
        == "menu"
    ]

      return menu_documents
    @staticmethod
    def build_menu_context(
      db: Session,
      item_name: str,
      question: str
):

    # -----------------------------
    # 1. Get live database data
    # -----------------------------

      menu_items = (
        MenuRetriever.search_menu_item(
            db,
            item_name
        )
    )

      database_context = []

      for item in menu_items:

        database_context.append(
            MenuRetriever.format_menu_item(
                item
            )
        )

    # -----------------------------
    # 2. Get PDF / FAISS data
    # -----------------------------

      documents = (
        MenuRetriever.get_detailed_information(
             item_name
        )
    )

      pdf_context = []

      for document in documents:

        pdf_context.append(
            document.page_content
        )

    # -----------------------------
    # 3. Return both sources
    # -----------------------------

      return {
        "database": database_context,
        "knowledge_base": pdf_context
    }

    @staticmethod
    def find_items_from_question(
      db: Session,
      question: str
):

      return MenuItemRepository.search_by_question(
        db,
        question
    )

    @staticmethod
    def find_category_from_question(
      db: Session,
      question: str
):

      from app.models.category import Category

      categories = (
        db.query(Category)
        .all()
    )

      question_lower = question.lower()

      matches = []
 
      for category in categories:

        if category.name.lower() in question_lower:

            matches.append(category)

      return matches
    @staticmethod
    def is_vegetarian_question(
      question: str
):

      text = question.lower()

      return (
        "vegetarian" in text
        or "veg" in text
    )