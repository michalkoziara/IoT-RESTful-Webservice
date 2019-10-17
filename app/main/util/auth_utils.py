import datetime
import jwt
from typing import Optional
from typing import Tuple

from app.main.util.constants import Constants


class Auth:

    @staticmethod
    def encode_auth_token(user_id: str, is_admin: bool) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'admin': is_admin
        }

        auth_token = jwt.encode(
            payload,
            Constants.SECRET_KEY,
            algorithm='HS256'
        )

        return auth_token.decode()

    @staticmethod
    def decode_auth_token(auth_token: str) -> Tuple[Optional[str], Optional[dict]]:
        try:
            payload = jwt.decode(auth_token, Constants.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Constants.RESPONSE_MESSAGE_SIGNATURE_EXPIRED, None
        except jwt.InvalidTokenError:
            return Constants.RESPONSE_MESSAGE_INVALID_TOKEN, None

        return None, payload

    @staticmethod
    def get_user_info_from_auth_header(auth_header: str) -> Tuple[Optional[str], Optional[dict]]:
        if auth_header:
            auth_header_parts = auth_header.split(" ")

            if len(auth_header_parts) == 2 and auth_header_parts[0] == 'Bearer':
                auth_token = auth_header_parts[1]
                result, token_payload = Auth.decode_auth_token(auth_token)

                if result is None:
                    try:
                        user_id = token_payload['sub']
                        admin = token_payload['admin']
                    except KeyError:
                        return Constants.RESPONSE_MESSAGE_INVALID_TOKEN, None

                    return None, {
                        'user_id': user_id,
                        'is_admin': admin
                    }
                else:
                    return result, None

        return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None
