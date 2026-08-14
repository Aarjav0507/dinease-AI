from sqlalchemy import String, Integer, DateTime,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.reservation import Reservation


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
)

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
)

    role: Mapped[str] = mapped_column(
        String(20),
         nullable=False,
         default="USER"
)

    is_active: Mapped[bool] = mapped_column(
         Boolean,
         default=True
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
    cart = relationship(
      "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
)
    reservations = relationship(
      "Reservation",
        back_populates="user"
)
    orders = relationship(
    "Order",
    back_populates="user"
)
    password_reset_token: Mapped[str] = mapped_column(
    String(255),
    nullable=True
)

    password_reset_token_expiry: Mapped[datetime] = mapped_column(
    DateTime,
    nullable=True
)