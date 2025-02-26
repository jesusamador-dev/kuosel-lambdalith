from pydantic import BaseModel
from typing import Optional
from datetime import date


class Saving(BaseModel):
    id: Optional[int] = None
    name: str
    target_amount: float
    start_date: date
    end_date: date
    user_id: str
    category_id: int
    priority: int = 1
    is_shared: bool = False
    deleted_at: Optional[date] = None

    class Config:
        from_attributes = True


class SavingProgress(BaseModel):
    id: int
    name: str
    target_amount: float
    current_amount: float
    remaining_amount: float
    start_date: date
    end_date: date
    category_id: int
    category_name: str
    priority: int
    is_shared: bool
