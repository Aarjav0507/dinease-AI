from datetime import datetime

from pydantic import BaseModel, Field


# -----------------------------
# Add Item To Cart
# -----------------------------
class AddToCartRequest(BaseModel):

    menu_item_id: int

    quantity: int = Field(
        default=1,
        gt=0
    )


# -----------------------------
# Update Quantity
# -----------------------------
class UpdateCartItemRequest(BaseModel):

    quantity: int = Field(
        ...,
        gt=0
    )


# -----------------------------
# Cart Item Response
# -----------------------------
class CartItemResponse(BaseModel):

    id: int

    menu_item_id: int

    quantity: int

    class Config:
        from_attributes = True


# -----------------------------
# Cart Response
# -----------------------------
class CartResponse(BaseModel):

    id: int

    user_id: int

    created_at: datetime

    updated_at: datetime

    cart_items: list[CartItemResponse]

    class Config:
        from_attributes = True