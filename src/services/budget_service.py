from src.db.repositories.budgets_repository import BudgetRepository


class BudgetService:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    async def create_budget(self, budget_data: dict):
        # Verificar si el usuario ya tiene un presupuesto
        existing_budget = await self.repository.get_budget_by_user(budget_data["user_id"])
        if existing_budget:
            raise ValueError("El usuario ya tiene un presupuesto creado. No se pueden crear más.")

        # Crear el presupuesto
        new_budget = await self.repository.insert_budget(budget_data)

        # Asociar categorías al presupuesto
        await self.repository.insert_budget_categories(new_budget.id, budget_data.get("categories", []))

        return {
            "id": new_budget.id,
            "name": new_budget.name,
            "amount": new_budget.amount,
            "budget_type": new_budget.budget_type,
            "start_date": new_budget.start_date,
            "end_date": new_budget.end_date,
            "user_id": new_budget.user_id,
            "is_favorite": new_budget.is_favorite,
            "categories": budget_data.get("categories", []),
            "created_at": new_budget.created_at,
            "updated_at": new_budget.updated_at,
        }

    async def get_budget(self, user_id: str):
        # Obtener el presupuesto único del usuario
        budget = await self.repository.get_budget_by_user(user_id)
        if not budget:
            raise ValueError("El usuario no tiene un presupuesto creado.")
        return budget
