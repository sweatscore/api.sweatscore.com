""" The entry point for the Sweatscore API """

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import database

# import library as applib

# from apps.ads.views import router as ads_router
# from apps.user.views import router as user_router
# from apps.account.views import router as account_router
# from apps.authorization.views import router as auth_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """ Initializes the application """

#     applib.open_logger()

#     database.create_dbengine(
#         applib.get_config_section('database'),
#         applib.DEBUG
#     )

#     app.include_router(ads_router)
#     app.include_router(auth_router)
#     app.include_router(user_router)
#     app.include_router(account_router)

#     yield


# app = FastAPI(title=applib.TITLE, lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    #allow_origins = applib.ALLOWED_ORIGINS,
    allow_origins = 'http://localhost:5173',
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

@app.get('/test')
async def test() -> str:
    return "SUCCESS"