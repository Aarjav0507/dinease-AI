from pydantic import BaseModel, Field
from datetime import datetime


# -----------------------------
# Create Category
# -----------------------------
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    image_url: str | None = None


# -----------------------------
# Update Category
# -----------------------------
class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    image_url: str | None = None
    is_active: bool | None = None


# -----------------------------
# Response Schema
# -----------------------------
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    image_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True