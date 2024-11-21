from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.core.security.cognito_service import CognitoService
from src.db.models.user import User
from src.db.repositories.user_repository import UserRepository
import time


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.cognito_service = CognitoService()
        self.user_repository = UserRepository(db)

    def register_user(self, username: str, email: str, password: str, additional_attributes: dict):
        # Registro en Cognito
        cognito_response = self.cognito_service.register_user(
            username=username,
            email=email,
            password=password,
            additional_attributes={
                "name": additional_attributes.get("name"),
                "updated_at": str(int(time.time())),
            }
        )

        # Registro en la base de datos
        new_user = User(
            id=cognito_response['UserSub'],
            name=additional_attributes.get("name"),
            email=email,
            country="MX",
            profile_image=None,  # Valor predeterminado
            subscription_type=None,  # Valor predeterminado
            subscription_status=None  # Valor predeterminado
        )

        # Intentar registrar al usuario en la base de datos
        try:
            self.user_repository.register_user_in_db(cognito_response['UserSub'], email, new_user)
        except Exception as e:
            # Si ocurre un error, eliminar el usuario en Cognito para mantener la consistencia
            self.cognito_service.delete_user(cognito_response['UserSub'])
            raise HTTPException(status_code=500, detail="Error registering user in the database") from e

        return {"message": "User registered successfully. Please confirm your email."}

    def confirm_user(self, username: str, confirmation_code: str):
        return self.cognito_service.confirm_user(
            username=username,
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

    def resend_confirmation_code(self, username: str):
        """Reenvía el código de confirmación al usuario."""
        try:
            return self.cognito_service.resend_confirmation_code(username=username)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error resending confirmation code") from e

