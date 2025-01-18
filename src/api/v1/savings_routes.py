from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date
from src.services.saving_service import SavingService
from src.db.models.saving import Saving, SavingProgress

router = APIRouter()

@router.post("/savings/", response_model=Saving)
async def create_saving(saving: Saving, savings_service: SavingService = Depends(SavingService)):
    saving_created = await savings_service.create_saving(saving)
    if saving_created:
        return saving_created
    raise HTTPException(status_code=400, detail="Error creating saving")

@router.put("/savings/{saving_id}", response_model=Saving)
async def update_saving(saving_id: int, saving: Saving, savings_service: SavingService = Depends(SavingService)):
    saving_updated = await savings_service.update_saving(saving_id, saving)
    if saving_updated:
        return saving_updated
    raise HTTPException(status_code=404, detail="Saving not found")

from typing import List

@router.get("/savings/progress/{user_id}", response_model=List[SavingProgress])
async def get_saving_progress(user_id: str, saving_id: Optional[int] = None, savings_service: SavingService = Depends(SavingService)):
    progress = await savings_service.get_saving_progress(user_id, saving_id)
    if progress:
        return progress
    raise HTTPException(status_code=404, detail="No saving progress found")

