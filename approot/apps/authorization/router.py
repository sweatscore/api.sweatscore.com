"""
    The Authorization router.
    Routes requests to authorization and security functions.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pydantic import (
    BaseModel,
    EmailStr)

from database import get_db_session

from . import library as lib


# Models

class SessionOut(BaseModel):
    token: str
    expiration: int


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class LoginOut(BaseModel):
    code: str
    message: str
    session_token: SessionOut | None = None


router = APIRouter(prefix='/auth')


@router.post('/login', response_model_exclude_none=True)
def login(request: LoginIn, dbsession: Session=Depends(get_db_session)) -> LoginOut:
    """
        Logs a user into Sweatscore, and returns a status code
        to indicate the success or failure of the operation.
    """

    return lib.login(request, dbsession)
