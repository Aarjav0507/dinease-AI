from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    razorpay_order_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    razorpay_payment_id: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    razorpay_signature: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    amount: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False
)


    payment_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
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

    order = relationship(
        "Order",
        back_populates="payment"
    )
    refund_amount: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False,
    default=0
)

    refund_status: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="NOT_APPLICABLE"
)
    refund_id: Mapped[str] = mapped_column(
    String(100),
    nullable=True
)