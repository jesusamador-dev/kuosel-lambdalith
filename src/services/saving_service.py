from src.db.models.saving import Saving
from src.db.repositories.savings_repository import SavingsRepository
from fastapi import HTTPException

class SavingService:
    def __init__(self, repository: SavingsRepository):
        self.repository = repository

    async def create_saving(self, saving: Saving) -> Saving:
        """Create a new saving goal."""
        try:
            return await self.repository.create_saving(saving)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_saving(self, saving_id: int, saving: Saving) -> Saving:
        """Update an existing saving goal."""
        existing_saving = await self.repository.get_saving_by_id(saving_id)
        if not existing_saving:
            raise HTTPException(status_code=404, detail="Saving not found")

        try:
            return await self.repository.update_saving(saving_id, saving)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_saving(self, saving_id: int) -> Saving:
        """Delete an existing saving goal."""
        existing_saving = await self.repository.get_saving_by_id(saving_id)
        if not existing_saving:
            raise HTTPException(status_code=404, detail="Saving not found")

        try:
            return await self.repository.delete_saving(saving_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_saving_progress(self, saving_id: int) -> Saving:
        """Retrieve a saving goal by its ID."""
        saving = await self.repository.get_saving_progress(saving_id)
        if not saving:
            raise HTTPException(status_code=404, detail="Saving not found")
        return saving
