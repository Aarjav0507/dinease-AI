from datetime import datetime, date, time
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    Numeric,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    table_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant_tables.id"),
        nullable=False
    )

    reservation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    guests_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

  

    reservation_charge: Mapped[Decimal] = mapped_column(
       Numeric(10, 2),
       default=Decimal("0.00"),
       nullable=False
)

    reservation_credit_remaining: Mapped[Decimal] = mapped_column(
       Numeric(10, 2),
       default=Decimal("0.00"),
       nullable=False
)

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="reservations"
    )

    table = relationship(
        "RestaurantTable",
        back_populates="reservations"
    )
    order = relationship(
    "Order",
    back_populates="reservation",
    uselist=False
)
    reservation_fee_waived = Column(
     Boolean,
      nullable=False,
      default=False
)