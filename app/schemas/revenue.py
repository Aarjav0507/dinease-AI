from pydantic import BaseModel


class RevenueResponse(BaseModel):
    gross_revenue: float
    refund_amount: float
    net_revenue: float
    total_refunds: int