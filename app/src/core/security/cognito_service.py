# app/core/security/cognito_service.py
import requests
from authlib.jose import jwt, JoseError
from fastapi import HTTPException
from app.src.core.config import settings


class CognitoService:
    def __init__(self):
        self.jwks_url = f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        self.jwks_keys = self._fetch_jwks_keys()

    def _fetch_jwks_keys(self):
        try:
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            return response.json()["keys"]
        except requests.RequestException as e:
            raise RuntimeError("Could not fetch JWKS keys") from e

    def verify_token(self, token: str):
        try:
            # Decodificar el encabezado para obtener el "kid"
            unverified_header = jwt.decode_header(token)
            rsa_key = next((key for key in self.jwks_keys if key["kid"] == unverified_header["kid"]), None)
            if rsa_key is None:
                raise HTTPException(status_code=403, detail="Invalid token header")

            # Verificar y decodificar el token JWT
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
            payload.validate()  # Valida las reclamaciones del token
            return payload  # Retorna el payload decodificado si el token es válido
        except JoseError:
            raise HTTPException(status_code=403, detail="Token is invalid or has expired")
