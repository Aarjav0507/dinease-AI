from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String,
    Numeric
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    reservation_id = Column(
        Integer,
        ForeignKey("reservations.id"),
        unique=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subtotal_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    reservation_charge = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    reservation_credit_used = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    payment_status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    order_status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    reservation = relationship(
        "Reservation",
        back_populates="order"
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    food_total_amount = Column(
      Numeric(10, 2),
       nullable=False,
       default=0
)
    payment = relationship(
      "Payment",
        back_populates="order",
        uselist=False
)