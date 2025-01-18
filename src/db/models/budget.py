from pydantic import BaseModel
from typing import List, Optional

class BudgetCategoryInput(BaseModel):
    id: int  # ID de la categoría (e.g., 1: Vivienda, 2: Comida)
    amount: float  # Monto asignado a la categoría

class BudgetCreate(BaseModel):
    user_id: str
    name: str
    amount: float
    budget_type: str  # Valores válidos: 'weekly', 'monthly', 'annual'
    start_date: Optional[str]  # Formato ISO (YYYY-MM-DD)
    is_favorite: Optional[bool] = False  # Si el presupuesto es marcado como favorito
    categories: List[BudgetCategoryInput]  # Categorías y sus montos

class BudgetCategoryOutput(BaseModel):
    id: int  # ID de la categoría
    amount: float  # Monto asignado a la categoría

class BudgetResponse(BaseModel):
    id: int
    name: str
    amount: float
    budget_type: str
    start_date: str
    end_date: str
    user_id: str
    is_favorite: bool
    categories: List[BudgetCategoryOutput]  # Categorías asociadas
    created_at: str  # Fecha de creación en formato ISO
    updated_at: str  # Fecha de última actualización en formato ISO


class BudgetDelete(BaseModel):
    budget_id: int  # ID del presupuesto a eliminar
    user_id: str  # ID del usuario propietario
