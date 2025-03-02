import base64
import hmac
import hashlib
import requests
from authlib.jose import jwt, JoseError
from fastapi import HTTPException
import boto3
from src.core.config import settings
from botocore.exceptions import BotoCoreError, ClientError


class CognitoService:
    def __init__(self):
        self.jwks_url = f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        self.jwks_keys = self._fetch_jwks_keys()
        self.client = boto3.client('cognito-idp', region_name=settings.AWS_REGION)

    def _fetch_jwks_keys(self):
        try:
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            return response.json()["keys"]
        except requests.RequestException as e:
            raise RuntimeError("Could not fetch JWKS keys") from e

    def verify_token(self, token: str):
        try:
            unverified_header = jwt.decode_header(token)
            rsa_key = next((key for key in self.jwks_keys if key["kid"] == unverified_header["kid"]), None)
            if rsa_key is None:
                raise HTTPException(status_code=403, detail="Invalid token header")

            public_key = {
                "kty": rsa_key["kty"],
                "kid": rsa_key["kid"],
                "use": rsa_key["use"],
                "n": rsa_key["n"],
                "e": rsa_key["e"]
            }

            payload = jwt.decode(
                token,
                public_key,
                claims_options={
                    "aud": {"essential": True, "value": settings.COGNITO_CLIENT_ID}
                }
            )
            payload.validate()
            return payload
        except JoseError:
            raise HTTPException(status_code=403, detail="Token is invalid or has expired")

    def _generate_secret_hash(self, username: str) -> str:
        """Calcula el SECRET_HASH usando Client Secret, Client ID y el nombre de usuario"""
        message = f"{username}{settings.COGNITO_CLIENT_ID}".encode("utf-8")
        key = settings.COGNITO_CLIENT_SECRET.encode("utf-8")
        secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode("utf-8")
        return secret_hash

    def register_user(self, username: str, email: str, password: str, additional_attributes: dict = None):
        try:
            attributes = [{"Name": "email", "Value": email}]
            # Incluye otros atributos si es necesario, solo si tienes permiso para ellos
            if additional_attributes:
                for key, value in additional_attributes.items():
                    attributes.append({"Name": key, "Value": value})

            secret_hash = self._generate_secret_hash(username)

            response = self.client.sign_up(
                ClientId=settings.COGNITO_CLIENT_ID,
                SecretHash=secret_hash,
                Username=username,  # Usa un nombre de usuario que no sea el correo electrónico
                Password=password,
                UserAttributes=attributes
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=400, detail=e.response['Error']['Message'])

        # Método para eliminar un usuario por su Username
    def delete_user(self, username: str):
        try:
            response = self.client.admin_delete_user(
                UserPoolId=settings.COGNITO_USER_POOL_ID,
                Username=username
            )
            return response
        except (BotoCoreError, ClientError) as e:
            raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")

    def confirm_user(self, username: str, confirmation_code: str):
        try:
            response = self.client.confirm_sign_up(
                ClientId=settings.COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code,
                SecretHash=self._generate_secret_hash(username)
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=400, detail=f"Error confirming user: {e.response['Error']['Message']}")

    def resend_confirmation_code(self, username: str):
        try:
            response = self.client.resend_confirmation_code(
                ClientId=settings.COGNITO_CLIENT_ID,
                Username=username,
                SecretHash=self._generate_secret_hash(username)
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=400,
                                detail=f"Error resending confirmation code: {e.response['Error']['Message']}")

    def login_user(self, email: str, password: str):
        try:
            auth_params = {
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": self._generate_secret_hash(email),
            }

            response = self.client.initiate_auth(
                ClientId=settings.COGNITO_CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters=auth_params,
            )

            return {
                "accessToken": response["AuthenticationResult"]["AccessToken"],
                "idToken": response["AuthenticationResult"]["IdToken"],
                "refreshToken": response["AuthenticationResult"]["RefreshToken"],
                "expiresIn": response["AuthenticationResult"]["ExpiresIn"],
                "tokenType": response["AuthenticationResult"]["TokenType"],
            }
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NotAuthorizedException":
                raise HTTPException(status_code=401, detail="Incorrect username or password.")
            elif error_code == "UserNotConfirmedException":
                raise HTTPException(status_code=403, detail="User is not confirmed.")
            elif error_code == "UserNotFoundException":
                raise HTTPException(status_code=404, detail="User does not exist.")
            else:
                raise HTTPException(status_code=500, detail=f"Login failed: {e.response['Error']['Message']}")

