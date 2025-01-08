from src.db.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepository):
        self.transaction_repo = transaction_repo

    async def create_transaction(self, transaction_data: dict):
        return await self.transaction_repo.insert_transaction(transaction_data)

    async def get_transaction(self, trans_id: int):
        transaction = await self.transaction_repo.select_transaction(trans_id)
        if not transaction:
            raise ValueError("Transacción no encontrada")
        return transaction

    async def update_transaction(self, trans_id: int, transaction_data: dict):
        return await self.transaction_repo.update_transaction(trans_id, transaction_data)

    async def delete_transaction(self, trans_id: int):
        return await self.transaction_repo.delete_transaction(trans_id)

    async def get_paginated_transactions(self, filters: dict):
        # Obtener datos crudos del repositorio
        raw_transactions = await self.transaction_repo.get_paginated_transactions(filters)

        # Transformar los datos en el formato deseado
        transactions = [
            {
                "id": row.id,
                "amount": row.amount,
                "description": row.description,
                "date": row.date,
                "user_id": row.user_id,
                "budget_id": row.budget_id,
                "savings_id": row.savings_id,
                "category": {
                    "id": row.category_id,
                    "name": row.category_name,
                    "ui_settings": row.category_ui_settings,
                },
                "type": row.type,
                "payment_method": row.payment_method,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in raw_transactions
        ]

        return transactions
