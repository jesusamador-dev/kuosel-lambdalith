from pydantic import BaseModel
from typing import Optional
from datetime import date


class TransactionBase(BaseModel):
    amount: Optional[float]
    description: Optional[str]
    date: Optional[date]
    user_id: Optional[str]
    budget_id: Optional[int]
    savings_id: Optional[int]
    category_id: Optional[int]
    type: Optional[str]
    payment_method: Optional[str]


class TransactionCreate(TransactionBase):
    amount: float
    date: date
    user_id: str
    type: str
    payment_method: str


class TransactionUpdate(TransactionBase):
    pass
