from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from sqlalchemy import func
from app.models.category import Category


class MenuItemRepository:

    @staticmethod
    def create(
        db: Session,
        menu_item: MenuItem
    ) -> MenuItem:

        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)

        return menu_item

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(MenuItem)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        menu_item_id: int
    ):

        return (
            db.query(MenuItem)
            .filter(
                MenuItem.id == menu_item_id
            )
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str
    ):

        return (
            db.query(MenuItem)
            .filter(
                MenuItem.name == name
            )
            .first()
        )

    @staticmethod
    def get_by_category(
        db: Session,
        category_id: int
    ):

        return (
            db.query(MenuItem)
            .filter(
                MenuItem.category_id == category_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        menu_item: MenuItem
    ) -> MenuItem:

        db.commit()
        db.refresh(menu_item)

        return menu_item

    @staticmethod
    def delete(
        db: Session,
        menu_item: MenuItem
    ):

        db.delete(menu_item)
        db.commit()

    @staticmethod
    def search_by_name(
      db: Session,
      name: str
):
      return (
        db.query(MenuItem)
        .filter(
            func.lower(MenuItem.name)
            .contains(name.lower())
        )
        .all()
    )

    @staticmethod
    def search_by_question(
      db: Session,
      question: str
):

      menu_items = (
        db.query(MenuItem)
        .all()
    )

      question_lower = question.lower()

      matches = []

      for item in menu_items:

        if item.name.lower() in question_lower:

            matches.append(item)

      return matches

    @staticmethod
    def get_by_category_name(
      db: Session,
      category_name: str
):

      return (
        db.query(MenuItem)
        .join(Category)
        .filter(
            func.lower(Category.name)
            == category_name.lower()
        )
        .all()
    )
    @staticmethod
    def get_vegetarian_by_category_name(
      db: Session,
      category_name: str
):

    

     return (
        db.query(MenuItem)
        .join(Category)
        .filter(
            func.lower(Category.name)
            == category_name.lower(),
            MenuItem.is_veg == True
        )
        .all()
    )