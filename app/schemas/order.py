from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_order_time: Decimal

    class Config:
        from_attributes = True

from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int

    reservation_id: int
    user_id: int

    subtotal_amount: Decimal

    reservation_charge: Decimal

    reservation_credit_used: Decimal

    total_amount: Decimal

    payment_status: str

    order_status: str

    created_at: datetime
    updated_at: datetime

    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    reservation_id: int