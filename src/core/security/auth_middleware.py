# app/core/security/auth_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
from src.core.security.cognito_service import CognitoService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.cognito_service = CognitoService()

    async def dispatch(self, request: Request, call_next):
        # Excluir rutas públicas, como documentación
        excluded_paths = ["/docs", "/openapi.json", "/api/v1/register", "/api/v1/login", "/api/v1/forgot-password",
                          "/api/v1/confirm-forgot-password"]

        # Verifica si la ruta actual está excluida
        if request.url.path in excluded_paths:
            return await call_next(request)

        # Verificar si existe el encabezado de autorización
        authorization: str = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

        # Obtener el token del encabezado y verificarlo
        token = authorization.split("Bearer ")[1]
        try:
            user = self.cognito_service.verify_token(token)
            request.state.user = user  # Almacena la información del usuario en el estado de la solicitud
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        # Llamar al siguiente middleware o endpoint si el token es válido
        response = await call_next(request)
        return response
