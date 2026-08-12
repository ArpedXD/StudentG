from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mysql.connector.pooling import MySQLConnectionPool
import os
from dotenv import load_dotenv
from websocketAPIreference import web_router
from api.signup import signup_router
from api.login import login_router
from api.Chat import chat_router
from Exceptions.DatabaseExceptions import FailedToConnectToDB


load_dotenv()

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("database... connecting..")

    try:
        app.state.pool = MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DATABASE"),
            user = os.getenv("DB_USERNAME"),
            password = os.getenv("DB_PASSWORD")
        )

        connection = app.state.pool.get_connection()

        if connection.is_connected():
            print("Connected")
        else:
            raise FailedToConnectToDB("Error, Failed to Connect To Database")
        
        connection.close()
    except FailedToConnectToDB as e:
        print(str(e))

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(web_router)
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(chat_router)