from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db.repositories.savings_repository import SavingsRepository
from src.services.saving_service import SavingService
from src.db.models.saving import Saving, SavingProgress

router = APIRouter()


def get_savings_repository(db: AsyncSession = Depends(get_db)) -> SavingsRepository:
    return SavingsRepository(db)


def get_savings_service(repo: SavingService = Depends(get_savings_repository)) -> SavingService:
    return SavingService(repository=repo)


@router.post("/savings/", response_model=Saving)
async def create_saving(saving: Saving, service: SavingService = Depends(get_savings_service)):
    saving_created = await service.create_saving(saving)
    if saving_created:
        return saving_created
    raise HTTPException(status_code=400, detail="Error creating saving")


@router.put("/savings/{saving_id}", response_model=Saving)
async def update_saving(saving_id: int, saving: Saving, service: SavingService = Depends(get_savings_service)):
    saving_updated = await service.update_saving(saving_id, saving)
    if saving_updated:
        return saving_updated
    raise HTTPException(status_code=404, detail="Saving not found")


@router.get("/savings/progress/{user_id}", response_model=List[SavingProgress])
async def get_saving_progress(
        saving_id: Optional[int] = None,
        service: SavingService = Depends(get_savings_service)):
    progress = await service.get_saving_progress(saving_id)
    if progress:
        return progress
    raise HTTPException(status_code=404, detail="No saving progress found")

