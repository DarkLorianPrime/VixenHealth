from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from routers.authentication.responses import Exceptions
from utils.jwt_utils import get_credentials_from_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        description = """
        Project authentication, based on the JWT.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error,
                                        description=description,
                                        scheme_name="JWTBearer")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(
            request
        )
        if credentials is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=Exceptions.INVALID_TOKEN_ACCESS)

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=Exceptions.BEARER_SCHEME_ERROR)

        payload = await get_credentials_from_token(credentials.credentials)
        request.state.jwt_payload = payload

        return bool(payload)
