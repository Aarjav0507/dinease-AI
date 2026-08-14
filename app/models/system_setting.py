from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        default=1
    )

    refund_percentage: Mapped[int] = mapped_column(
        Integer,
        default=80
    )

    cancellation_window_hours: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    reservation_charge_per_hour_per_guest: Mapped[int] = mapped_column(
        Integer,
        default=20
    )

    food_bill_threshold: Mapped[int] = mapped_column(
        Integer,
        default=1000
    )

    food_addition_cutoff_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30
    )