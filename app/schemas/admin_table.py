from pydantic import BaseModel


class TableCreate(BaseModel):
    table_number: str
    capacity: int


class TableUpdate(BaseModel):
    table_number: str
    capacity: int


class TableAvailabilityUpdate(BaseModel):
    is_active: bool