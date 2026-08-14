from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_users: int
    total_reservations: int
    total_orders: int
    total_payments: int
    total_revenue: float