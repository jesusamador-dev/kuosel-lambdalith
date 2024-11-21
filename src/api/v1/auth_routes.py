from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.services.user_service import UserService
from src.db.database import get_db

router = APIRouter()


# Modelos de datos para las solicitudes
class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str
    additional_attributes: dict = None


class ConfirmUserRequest(BaseModel):
    username: str
    confirmation_code: str


class LoginUserRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ConfirmForgotPasswordRequest(BaseModel):
    email: str
    confirmation_code: str
    new_password: str


class ResendConfirmationRequest(BaseModel):
    username: str


# Ruta para registro de usuario
@router.post("/register")
async def register_user(request: RegisterUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.register_user(
        username=request.username,
        email=request.email,
        password=request.password,
        additional_attributes=request.additional_attributes
    )


# Ruta para confirmación de usuario
@router.post("/confirm")
async def confirm_user(request: ConfirmUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.confirm_user(
        username=request.username,
        confirmation_code=request.confirmation_code
    )


# Ruta para login de usuario
@router.post("/login")
async def login_user(request: LoginUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login_user(
        email=request.email,
        password=request.password
    )


# Ruta para solicitud de recuperación de contraseña
@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.forgot_password(request.email)


# Ruta para confirmación de recuperación de contraseña
@router.post("/confirm-forgot-password")
async def confirm_forgot_password(request: ConfirmForgotPasswordRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.confirm_forgot_password(
        email=request.email,
        confirmation_code=request.confirmation_code,
        new_password=request.new_password
    )


# Ruta para reenviar el código de confirmación
@router.post("/resend-confirmation")
async def resend_confirmation_code(request: ResendConfirmationRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.resend_confirmation_code(username=request.username)
