import time
from typing import Dict, Optional
from datetime import datetime, timedelta, UTC

import jwt
from jwt.exceptions import PyJWTError

from app.config.config import Settings


def token_response(token: str) -> Dict[str, str]:
    return {"access_token": token}


secret_key = Settings().secret_key


def sign_jwt(user_id: str) -> Dict[str, str]:
    # Set the expiry time using timezone-aware UTC datetime
    expiration = datetime.now(UTC) + timedelta(minutes=40)  # 2400 seconds = 40 minutes
    payload = {
        "user_id": user_id,
        "expires": expiration.timestamp(),
        "iat": datetime.now(UTC).timestamp()  # issued at timestamp
    }
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> Optional[Dict]:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        return None
    except PyJWTError:
        return None