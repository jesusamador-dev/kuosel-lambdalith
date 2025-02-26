from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class BudgetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_budget_by_user(self, user_id: str):
        query = text("""
            SELECT * FROM manage_budgets(
                action := 'SELECT',
                p_user_id := :user_id
            );
        """)
        result = await self.db.execute(query, {"user_id": user_id})
        return result.fetchone()

    async def insert_budget(self, budget_data: dict):
        query = text("""
            SELECT * FROM manage_budgets(
                action := 'INSERT',
                p_user_id := :user_id,
                p_name := :name,
                p_amount := :amount,
                p_budget_type := :budget_type,
                p_start_date := :start_date,
                p_is_favorite := :is_favorite,
                p_auto_generate := :auto_generate
            );
        """)
        result = await self.db.execute(query, budget_data)
        return result.fetchone()

    async def insert_budget_categories(self, budget_id: int, categories: list):
        query = text("""
            INSERT INTO budget_categories (budget_id, category_id, amount)
            VALUES (:budget_id, :category_id, :amount)
        """)
        for category in categories:
            await self.db.execute(query, {
                "budget_id": budget_id,
                "category_id": category["id"],
                "amount": category["amount"]
            })
        await self.db.commit()
