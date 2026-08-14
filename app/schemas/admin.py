from pydantic import BaseModel


class OrderStatusUpdate(BaseModel):
    order_status: str