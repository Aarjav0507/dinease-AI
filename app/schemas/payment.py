from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    order_id: int


class CreatePaymentResponse(BaseModel):

    payment_id: int

    razorpay_order_id: str

    amount: Decimal

    payment_status: str

    class Config:
        from_attributes = True


class VerifyPaymentRequest(BaseModel):

    razorpay_order_id: str

    razorpay_payment_id: str

    razorpay_signature: str


class PaymentResponse(BaseModel):

    id: int

    order_id: int

    razorpay_order_id: str

    razorpay_payment_id: str | None

    amount: Decimal

    payment_status: str

    refund_amount: Decimal

    refund_status: str

    created_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel


class PaymentVerifyRequest(BaseModel):

    razorpay_order_id: str

    razorpay_payment_id: str

    razorpay_signature: str