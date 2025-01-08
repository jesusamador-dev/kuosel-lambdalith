from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class TransactionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def insert_transaction(self, transaction_data: dict):
        query = text("""
            SELECT * FROM manage_transactions(
                action := 'INSERT',
                p_amount := :amount,
                p_description := :description,
                p_date := :date,
                p_user_id := :user_id,
                p_budget_id := :budget_id,
                p_savings_id := :savings_id,
                p_category_id := :category_id,
                p_type := :type,
                p_payment_method := :payment_method
            );
        """)
        result = await self.db_session.execute(query, transaction_data)
        return result.fetchone()

    async def select_transaction(self, trans_id: int):
        query = text("""
            SELECT * FROM manage_transactions(
                action := 'SELECT',
                trans_id := :trans_id
            );
        """)
        result = await self.db_session.execute(query, {"trans_id": trans_id})
        return result.fetchone()

    async def update_transaction(self, trans_id: int, transaction_data: dict):
        query = text("""
            SELECT * FROM manage_transactions(
                action := 'UPDATE',
                trans_id := :trans_id,
                p_amount := :amount,
                p_description := :description,
                p_date := :date,
                p_user_id := :user_id,
                p_budget_id := :budget_id,
                p_savings_id := :savings_id,
                p_category_id := :category_id,
                p_type := :type,
                p_payment_method := :payment_method
            );
        """)
        result = await self.db_session.execute(query, {"trans_id": trans_id, **transaction_data})
        return result.fetchone()

    async def delete_transaction(self, trans_id: int):
        query = text("""
            SELECT * FROM manage_transactions(
                action := 'DELETE',
                trans_id := :trans_id
            );
        """)
        result = await self.db_session.execute(query, {"trans_id": trans_id})
        return result.fetchone()

    async def get_paginated_transactions(self, filters: dict):
        query = text("""
            SELECT * FROM get_paginated_transactions(
                p_user_id := :user_id,
                p_budget_id := :budget_id,
                p_category_id := :category_id,
                p_type := :type,
                p_start_date := :start_date,
                p_end_date := :end_date,
                p_page := :page,
                p_page_size := :page_size
            );
        """)
        result = await self.db_session.execute(query, filters)
        return result.fetchall()
