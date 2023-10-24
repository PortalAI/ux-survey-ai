from typing import Protocol
from fastapi import HTTPException

from fastapi_cognito import CognitoToken
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


class UserRelatedEntity(Protocol):
    user_id: list[str]


class Auth:
    @staticmethod
    def has_permission(entity: UserRelatedEntity, auth: CognitoToken) -> bool:
        # todo: return True for admin
        # todo: return False is user deactivated/deleted
        return auth.username in entity.user_id

    @staticmethod
    def validate_permission(entity: UserRelatedEntity, auth: CognitoToken) -> bool:
        if entity is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Entity not found")
        if not Auth.has_permission(entity, auth):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"{auth.username=} does not own this entity")
        return True

