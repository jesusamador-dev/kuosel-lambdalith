# app/db/repositories/user_repository.py
from sqlalchemy.orm import Session
from app.src.db.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def register_user_in_db(self, user_id: str, user_email: str, user_data: dict):
        try:
            self.db.execute(
                "CALL sp_register_user(:user_id, :user_email, :user_name, :user_country, :user_profile_image, :user_subscription_type, :user_subscription_status)",
                {
                    "user_id": user_id,
                    "user_email": user_email,
                    "user_name": user_data.get("name"),
                    "user_country": user_data.get("country"),
                    "user_profile_image": user_data.get("profile_image"),
                    "user_subscription_type": user_data.get("subscription_type"),
                    "user_subscription_status": user_data.get("subscription_status"),
                }
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
