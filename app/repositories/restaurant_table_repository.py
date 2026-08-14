from sqlalchemy.orm import Session

from app.models.restaurant_table import RestaurantTable


class RestaurantTableRepository:

    @staticmethod
    def create(
        db: Session,
        table: RestaurantTable
    ) -> RestaurantTable:

        db.add(table)
        db.commit()
        db.refresh(table)

        return table

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            RestaurantTable
        ).all()

    @staticmethod
    def get_by_id(
        db: Session,
        table_id: int
    ):

        return db.query(
            RestaurantTable
        ).filter(
            RestaurantTable.id == table_id
        ).first()

    @staticmethod
    def get_by_table_number(
        db: Session,
        table_number: str
    ):

        return db.query(
            RestaurantTable
        ).filter(
            RestaurantTable.table_number == table_number
        ).first()

    @staticmethod
    def delete(
        db: Session,
        table: RestaurantTable
    ):

        db.delete(table)
        db.commit()
    @staticmethod
    def update(
      db: Session,
      table: RestaurantTable
):
      db.commit()
      db.refresh(table)

      return table