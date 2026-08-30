from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    # These rules validate expense data before it reaches the database.
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category: str = Field(min_length=1, max_length=100)
    expense_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    # Allow Pydantic to build a response from a SQLAlchemy Expense object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
