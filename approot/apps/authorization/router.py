"""
    The Authorization router.
    Routes requests to log-in and sign-up functions.
"""

from fastapi import APIRouter

from pydantic import (
    BaseModel,
    Field,
    EmailStr)

# Models

class LoginIn(BaseModel):
    username: str
    password: str


router = APIRouter(prefix='/auth')


@router.post('/login', response_model_exclude_none=True)
# def login(request: LoginIn, dbsession: Session=Depends(get_db_session)) -> LoginOut:
def login(request: LoginIn) -> str:
    """
        Logs a user into DigiAdsApp, or returns a status to initiate
        the sign-up process if the user doesn't exist in our database.
    """

    # return lib.login(request, dbsession)
