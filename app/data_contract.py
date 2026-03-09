from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, PositiveFloat, PositiveInt, field_validator


class CategoryEnum(str, Enum):
    book_category = "Books"
    elec_category = "Electronics"
    furn_category = "Furniture"


class Orders(BaseModel):
    customer_email: EmailStr
    order_date: datetime
    order_value: PositiveFloat
    product: str
    quantity: PositiveInt
    category: CategoryEnum

    @field_validator("category")
    def category_in_enum(cls, error):
        return error
