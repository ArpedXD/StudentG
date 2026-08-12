from fastapi import Cookie, APIRouter, Request
from schemas.SignupSchema import signup_information
from services.authenticateService import authenticateService


signup_router = APIRouter(prefix="/account")

class Signup:
    @signup_router.post("/signup")
    async def signup(request: Request, signup: signup_information, session: str = Cookie(None)):
        return authenticateService.signupservice(request, signup, session)