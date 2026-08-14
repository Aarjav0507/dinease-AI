from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem


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