""" The entry point for the Sweatscore API """

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import library as applib

from apps.signup.router import router as signup_router
# from apps.user.views import router as user_router
# from apps.account.views import router as account_router
# from apps.authorization.views import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Initializes the application """

#     applib.open_logger()

    app.include_router(signup_router)
#     app.include_router(auth_router)
#     app.include_router(user_router)
#     app.include_router(account_router)

    yield


app = FastAPI(title=applib.TITLE, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = applib.ALLOWED_ORIGINS,
    allow_credentials = False,
    allow_methods = ['GET', 'POST', 'OPTIONS'],
    allow_headers = ['*'],
)


@app.get('/')
async def get_index() -> dict:
    return {
        "version": "0.0.1",
        "name": "ALPHA",
        "build": 1,
        "date": "01/27/24",
        "time": "13:00:00"
    }
