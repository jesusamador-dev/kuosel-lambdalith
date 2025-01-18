from sqlalchemy.sql import text
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.saving import Saving, SavingProgress
from typing import Optional


class SavingsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_saving(self, saving: Saving) -> Saving:
        query = text("""
            SELECT * FROM manage_saving(
                'INSERT', NULL, :name, :target_amount, :start_date,
                :end_date, :user_id, :category_id, :priority, :is_shared
            );
        """)
        result = await self.db_session.execute(query, {
            'name': saving.name,
            'target_amount': saving.target_amount,
            'start_date': saving.start_date,
            'end_date': saving.end_date,
            'user_id': saving.user_id,
            'category_id': saving.category_id,
            'priority': saving.priority,
            'is_shared': saving.is_shared
        })
        await self.db_session.commit()
        return Saving.parse_obj(result.fetchone())

    async def update_saving(self, saving_id: int, saving: Saving) -> Saving:
        query = text("""
            SELECT * FROM manage_saving(
                'UPDATE', :id, :name, :target_amount, :start_date,
                :end_date, :user_id, :category_id, :priority, :is_shared
            );
        """)
        result = await self.db_session.execute(query, {
            'id': saving_id,
            'name': saving.name,
            'target_amount': saving.target_amount,
            'start_date': saving.start_date,
            'end_date': saving.end_date,
            'user_id': saving.user_id,
            'category_id': saving.category_id,
            'priority': saving.priority,
            'is_shared': saving.is_shared
        })
        await self.db_session.commit()
        return Saving.parse_obj(result.fetchone())

    async def delete_saving(self, saving_id: int) -> Saving:
        query = text("""
            SELECT * FROM manage_saving(
                'DELETE', :id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
            );
        """)
        result = await self.db_session.execute(query, {'id': saving_id})
        await self.db_session.commit()
        return Saving.parse_obj(result.fetchone())

    async def get_saving_progress(self, user_id: str, saving_id: Optional[int] = None) -> List[SavingProgress]:
        query = text("""
            SELECT * FROM get_saving_progress(
                p_user_id := :user_id,
                p_saving_id := :saving_id
            );
        """)
        result = await self.db_session.execute(query, {'user_id': user_id, 'saving_id': saving_id})
        savings_progress = result.fetchall()
        return [SavingProgress.from_orm(row) for row in savings_progress]

    async def get_saving_by_id(self, saving_id: int) -> Optional[Saving]:
        query = text("""
            SELECT id, name, target_amount, start_date, end_date, user_id, 
                   category_id, priority, is_shared, current_amount
            FROM savings
            WHERE id = :saving_id
        """)
        result = await self.db_session.execute(query, {'saving_id': saving_id})
        saving = result.fetchone()
        if saving:
            return Saving.parse_obj(saving)
        return None
