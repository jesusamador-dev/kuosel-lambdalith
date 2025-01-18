from fastapi import FastAPI
from mangum import Mangum
from src.core.security.auth_middleware import AuthMiddleware
from src.api.v1.auth_routes import router as auth_router
from src.api.v1.budgets_routes import router as budget_router
from src.api.v1.transactions_routes import router as transaction_router
from src.api.v1.savings_routes import router as saving_router

app = FastAPI()

# Añadir el middleware de autenticación para rutas protegidas
app.add_middleware(AuthMiddleware)

# Incluir las rutas de autenticación
app.include_router(auth_router, prefix="/v1")
app.include_router(budget_router, prefix="/v1")
app.include_router(transaction_router, prefix="/v1")
app.include_router(saving_router, prefix="/v1")

# Configurar handler para AWS Lambda
handler = Mangum(app)
