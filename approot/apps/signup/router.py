"""
    The Sign-up router.
    Routes requests to the sign-up functions.
"""

from fastapi import APIRouter, Response, status

from pydantic import (
    BaseModel,
    Field,
    EmailStr)

# Models

class NewUser(BaseModel):
    email: str
    password: str


router = APIRouter(prefix='/signup')


@router.post('/new-user', response_model_exclude_none=True)
# def login(request: LoginIn, dbsession: Session=Depends(get_db_session)) -> LoginOut:
def login(request: NewUser, response: Response) -> str:
    """
        
    """

    response.status_code = status.HTTP_304_NOT_MODIFIED
    return "NEW USER"
    # return lib.login(request, dbsession)
