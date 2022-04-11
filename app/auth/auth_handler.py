import time
import jwt
from typing import Dict
from decouple import config  # for read from env


JWT_SECRET = config("secret")  # setted in .env
JWT_ALGORITHM = config("algorithm")  # setted in .env


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(Emailaddr: str) -> Dict[str, str]:
    payload = {
        "Emailaddr": Emailaddr,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return {}
