from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.core.security.cognito_service import CognitoService
from app.src.db.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.cognito_service = CognitoService()
        self.user_repository = UserRepository(db)

    def register_user(self, email: str, password: str, additional_attributes: dict):
        # Registrar al usuario en Cognito
        cognito_response = self.cognito_service.register_user(
            email=email,
            password=password,
            additional_attributes=additional_attributes
        )

        # Extraer el ID de usuario de Cognito
        cognito_user_id = cognito_response["UserSub"]

        # Preparar datos del usuario para el stored procedure
        user_data = {
            "name": additional_attributes.get("name"),
            "country": additional_attributes.get("country"),
            "profile_image": additional_attributes.get("profile_image"),
            "subscription_type": additional_attributes.get("subscription_type"),
            "subscription_status": additional_attributes.get("subscription_status"),
        }

        # Intentar registrar al usuario en la base de datos
        try:
            self.user_repository.register_user_in_db(cognito_user_id, email, user_data)
        except Exception as e:
            # Si ocurre un error, eliminar el usuario en Cognito para mantener la consistencia
            self.cognito_service.delete_user(cognito_user_id)
            raise HTTPException(status_code=500, detail="Error registering user in the database") from e

        return {"message": "User registered successfully. Please confirm your email."}

    def confirm_user(self, email: str, confirmation_code: str):
        return self.cognito_service.confirm_user(
            email=email,
            confirmation_code=confirmation_code
        )

    def login_user(self, email: str, password: str):
        return self.cognito_service.login_user(
            email=email,
            password=password
        )

    def forgot_password(self, email: str):
        return self.cognito_service.forgot_password(email)

    def confirm_forgot_password(self, email: str, confirmation_code: str, new_password: str):
        return self.cognito_service.confirm_forgot_password(
            email=email,
            confirmation_code=confirmation_code,
            new_password=new_password
        )
