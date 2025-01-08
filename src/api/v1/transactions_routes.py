from fastapi import APIRouter, HTTPException, Depends, Query
from src.services.transaction_service import TransactionService
from src.db.models.transaction import TransactionCreate, TransactionUpdate

router = APIRouter()


@router.post("/transactions", status_code=201)
async def create_transaction(transaction: TransactionCreate, service: TransactionService = Depends()):
    try:
        new_transaction = await service.create_transaction(transaction.dict())
        return {"message": "Transacción registrada con éxito", "transaction": new_transaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions/{trans_id}")
async def get_transaction(trans_id: int, service: TransactionService = Depends()):
    try:
        transaction = await service.get_transaction(trans_id)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/transactions/{trans_id}")
async def update_transaction(trans_id: int, transaction: TransactionUpdate, service: TransactionService = Depends()):
    try:
        updated_transaction = await service.update_transaction(trans_id, transaction.dict(exclude_unset=True))
        return {"message": "Transacción actualizada con éxito", "transaction": updated_transaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/transactions/{trans_id}")
async def delete_transaction(trans_id: int, service: TransactionService = Depends()):
    try:
        deleted_transaction = await service.delete_transaction(trans_id)
        return {"message": "Transacción eliminada con éxito", "transaction": deleted_transaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions")
async def list_transactions(
    user_id: str,
    budget_id: int = Query(None),
    category_id: int = Query(None),
    type: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: TransactionService = Depends()
):
    filters = {
        "user_id": user_id,
        "budget_id": budget_id,
        "category_id": category_id,
        "type": type,
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
    }
    try:
        transactions = await service.get_paginated_transactions(filters)
        return {"transactions": transactions, "page": page, "page_size": page_size}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
