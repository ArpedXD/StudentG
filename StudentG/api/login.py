from fastapi import APIRouter, Cookie, Request
from schemas.LoginSchema import login_information
from services.authenticateService import authenticateService
from repositories.SessionDB import SessionDB

login_router = APIRouter(prefix="/account")

class Login:
    @login_router.post("/login")
    async def login(request: Request, login: login_information, session_id: str = Cookie(None)):
        return authenticateService.loginservice(request, login, session_id)