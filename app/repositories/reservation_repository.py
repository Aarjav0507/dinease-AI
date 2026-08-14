from datetime import date, time

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reservation import Reservation



class ReservationRepository:

    @staticmethod
    def create(
        db: Session,
        reservation: Reservation
    ):

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def get_by_id(
        db: Session,
        reservation_id: int
    ):

        return db.query(
            Reservation
        ).filter(
            Reservation.id == reservation_id
        ).first()

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            Reservation
        ).all()

    @staticmethod
    def get_user_reservations(
        db: Session,
        user_id: int
    ):

        return db.query(
            Reservation
        ).filter(
            Reservation.user_id == user_id
        ).all()

    @staticmethod
    def get_overlapping_reservation(
        db: Session,
        table_id: int,
        reservation_date: date,
        start_time: time,
        end_time: time
    ):

        return (
            db.query(Reservation)
            .filter(
                Reservation.table_id == table_id,
                Reservation.reservation_date == reservation_date,
                Reservation.status.in_(
                    ["PENDING_PAYMENT", "CONFIRMED", "ACTIVE"]
                ),
                Reservation.start_time < end_time,
                Reservation.end_time > start_time
            )
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        reservation: Reservation
    ):

        db.delete(reservation)
        db.commit()

    @staticmethod
    def update(
       db: Session,
       reservation: Reservation
):
        db.commit()
        db.refresh(reservation)
        return reservation
    @staticmethod
    def count_reservations(
       db: Session
):
      return db.query(Reservation).count()

