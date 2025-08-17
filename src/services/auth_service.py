from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.settings import settings


class AuthService:
    def __init__(self, pwd_context: CryptContext) -> None:
        self.pwd_context = pwd_context

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def authenticate_user(self, password: str, user_hashed_password: str) -> bool:
        if not self.verify_password(password, user_hashed_password):
            return False
        return True

    @staticmethod
    def encode_access_token(
        user_id: int, email: str, full_name: str, user_type: str
    ) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(days=30)
        payload = {
            "iat": now,
            "exp": exp,
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "type": user_type,
        }
        token = jwt.encode(payload, settings.SECRET_JWT, algorithm="HS256")
        return token

    @staticmethod
    def decode_access_token(token: str) -> dict[str, Any]:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_JWT, algorithms=["HS256"])
            payload = {
                "iat": decoded_token["iat"],
                "exp": decoded_token["exp"],
                "user_id": decoded_token["user_id"],
                "full_name": decoded_token["full_name"],
                "email": decoded_token["email"],
                "type": decoded_token["type"],
            }
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(status_code=403, detail="Token expired") from exc
        except jwt.InvalidTokenError as exc:
            raise HTTPException(status_code=403, detail="Invalid token") from exc
