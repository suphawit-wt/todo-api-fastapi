from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

import bcrypt
import jwt
from fastapi.security import HTTPBearer

from todo_api.core.settings import JWT_ALGORITHM, JWT_AUDIENCE, JWT_ISSUER, JWT_SECRET

auth_scheme = HTTPBearer(auto_error=False)


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


def generate_access_token(user_id: int, role: UserRole) -> str:
    issued_at: datetime = datetime.now(timezone.utc)
    expires: datetime = issued_at + timedelta(hours=12)
    payload: dict[str, Any] = {
        "sub": user_id,
        "iat": issued_at,
        "exp": expires,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "role": role.value,
    }
    return jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_token_payload(token: str) -> Any:
    return jwt.decode(
        jwt=token,
        key=JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        issuer=JWT_ISSUER,
        audience=JWT_AUDIENCE,
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def validate_password(req_password: str, user_password: str) -> bool:
    return bcrypt.checkpw(req_password.encode("utf-8"), user_password.encode("utf-8"))
