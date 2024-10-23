"""
    The signup router.
    Routes requests to the sign-up functions.
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


class NewUserIn(BaseModel):
    email: EmailStr
    password: str


class NewUserOut(BaseModel):
    code: str
    message: str
    session_token: SessionOut | None = None


class VerifyEmailIn(BaseModel):
    code: str


class VerifyEmailOut(BaseModel):
    code: str
    message: str


router = APIRouter(prefix='/signup')


@router.post('/new-user')
def new_user(request: NewUserIn, dbsession: Session=Depends(get_db_session)) -> NewUserOut:
    """
        Accepts the email and password from a request to create a new user account.
        Creates a new record in the users table if non exists.
        Returns an appropriate status code redirecting the user if the account needs to
        be verified or if the user is already verified.
    """

    return lib.new_user(request, dbsession)


@router.post('/verify-email')
def verify_email_address(request: VerifyEmailIn, dbsession: Session=Depends(get_db_session)) -> VerifyEmailOut:
    """
        Accepts a code that was sent to a new users email address from the request and
        verifies it against the code stored in the database.    
    """

    return lib.verify_email_address(request, dbsession)
