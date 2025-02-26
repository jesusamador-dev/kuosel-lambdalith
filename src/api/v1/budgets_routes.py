from fastapi import APIRouter, HTTPException, Depends
from src.db.models.budget import BudgetCreate, BudgetResponse
from src.services.budget_service import BudgetService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.budgets_repository import BudgetRepository
from src.db.database import get_db

router = APIRouter()


def get_budget_repository(db: AsyncSession = Depends(get_db)) -> BudgetRepository:
    return BudgetRepository(db)


def get_budget_service(repo: BudgetRepository = Depends(get_budget_repository)) -> BudgetService:
    return BudgetService(repository=repo)


@router.post("/budgets", response_model=BudgetResponse, status_code=201)
async def create_budget(budget: BudgetCreate, service: BudgetService = Depends(get_budget_service)):
    try:
        new_budget = await service.create_budget(budget.dict())
        return new_budget
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/budgets", response_model=BudgetResponse)
async def get_budget(user_id: str, service: BudgetService = Depends(get_budget_service)):
    try:
        budget = await service.get_budget(user_id)
        return budget
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
