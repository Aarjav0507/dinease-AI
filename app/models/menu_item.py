from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    preparation_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    calories: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    spice_level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )

    rating: Mapped[Decimal] = mapped_column(
        Numeric(2, 1),
        default=0.0,
        nullable=False
    )

    is_veg: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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

    category = relationship(
        "Category",
        back_populates="menu_items"
    )
    cart_items = relationship(
        "CartItem",
        back_populates="menu_item",
        
    )
    order_items = relationship(
    "OrderItem",
    back_populates="menu_item"
)