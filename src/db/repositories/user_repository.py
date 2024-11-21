from sqlalchemy.orm import Session
from src.db.models.user import User
from sqlalchemy import text


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def register_user_in_db(self, user_id: str, user_email: str, user_data: User):

        try:
            self.db.execute(
                text("SELECT fn_register_user(:user_id, :user_email, :user_name, :user_country, :user_profile_image, :user_subscription_type, :user_subscription_status)"),
                {
                    "user_id": user_id,
                    "user_email": user_email,
                    "user_name": user_data.name,
                    "user_country": user_data.country,
                    "user_profile_image": user_data.profile_image,
                    "user_subscription_type": user_data.subscription_type,
                    "user_subscription_status": user_data.subscription_status,
                }
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
