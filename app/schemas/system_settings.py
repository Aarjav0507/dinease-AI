from typing import Optional

from pydantic import BaseModel


class SystemSettingsUpdate(BaseModel):

    refund_percentage: Optional[int] = None

    cancellation_window_hours: Optional[int] = None

    reservation_charge_per_hour_per_guest: Optional[int] = None

    food_bill_threshold: Optional[int] = None

    food_addition_cutoff_minutes: Optional[int] = None