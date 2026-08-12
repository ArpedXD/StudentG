from fastapi import APIRouter, Request, Cookie, WebSocket, WebSocketDisconnect, Body
from schemas.ChatScema import GROUPCHAT
from services.ChatFunctionality import ChatFunctionality
from services.ChatSocket import WebsocketRepo
from repositories.SessionDB import SessionDB
from services.GroupService import GroupService
chat_router = APIRouter(prefix="/chat")
from pydantic import BaseModel
import json

class Base(BaseModel):
    value : str

class chat:
    global activeUsers
    activeUsers = {
        
    }

    @chat_router.get("/isLoggedin")
    async def isLoggedIn(request : Request, session_id : str = Cookie(None)):
        print("Hi")
        return SessionDB(request).verifySession(session_id)
    
    @chat_router.post("/test")
    async def test(base: Base):
        print(base.value + " read")
        users_success = set()
        for group_id in activeUsers:
            for user_id in activeUsers[group_id].values():
                if user_id in users_success:
                    return
                users_success.add(user_id)
                await user_id.send_text(json.dumps({
                    "username":"Announcement",
                    "message" : base.value,
                }))


    @chat_router.post("/create")
    async def create(request : Request, group_chat : GROUPCHAT, session_id : str = Cookie(None)):
        return ChatFunctionality.CreateGroupChat(request, group_chat, session_id)

    @chat_router.get("/Groupload")
    async def pageload(request: Request, session_id: str = Cookie(None)):
        return ChatFunctionality.GetGroupChat(request, session_id)

    @chat_router.websocket("/connect")
    async def chat(websocket: WebSocket, chat: str | None = None, session_id: str = Cookie(None)):
        await WebsocketRepo.Websocket(websocket, chat, session_id, activeUsers)

    @chat_router.get("/load_messages")
    async def load_message(request : Request, chat : int | None = None, session_id: str = Cookie(None), messages: int | None = None, before: int | None = None):
        return ChatFunctionality.load_chats(request, session_id, chat, messages, before)

    # <-------------------------------> GROUP CHAT API's
    @chat_router.post("/search_user")
    async def search_user(request : Request, text: str = Body(..., media_type="text/plain")):
        return GroupService.search_user(request, text)

    @chat_router.get("/showMembers")
    async def showMembers(request : Request, chat : int | None = None, session_id :str = Cookie(None)):
        return GroupService.load_members(request, chat, session_id)

    @chat_router.get("/isAdmin")
    async def checkIfAdmin(request: Request, chat : int, session_id: str = Cookie(None)):
        return GroupService.isAdmin(request, chat, session_id)

    @chat_router.get("/invite")
    async def InviteUser(request: Request, chat : int | None = None, target_user : int | None = None, session_id: str = Cookie(None)):
        return GroupService.inviteUser(request, chat, target_user,session_id)

    @chat_router.get("/remove")
    async def removeUser(request: Request, chat : int | None = None, target_user: int | None = None, session_id : str = Cookie(None)):
        return GroupService.removeuser(request, chat, target_user, session_id)