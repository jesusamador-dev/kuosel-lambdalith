from fastapi import APIRouter, HTTPException, Depends
from src.db.models.budget import BudgetCreate, BudgetResponse
from src.services.budget_service import BudgetService

router = APIRouter()

@router.post("/budgets", response_model=BudgetResponse, status_code=201)
async def create_budget(budget: BudgetCreate, service: BudgetService = Depends()):
    try:
        new_budget = await service.create_budget(budget.dict())
        return new_budget
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/budgets", response_model=BudgetResponse)
async def get_budget(user_id: str, service: BudgetService = Depends()):
    try:
        budget = await service.get_budget(user_id)
        return budget
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
