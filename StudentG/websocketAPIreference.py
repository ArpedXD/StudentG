from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

web_router = APIRouter(prefix="/main")

class Message(BaseModel):
    message : str

@web_router.websocket("/ws")
async def websocketTest(websocket : WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_json()
        chat = Message(**data)
        print(chat.message)
        print("HEY!")

        await websocket.send_json({
            "username": "Arped",
            "message": "Hello JS"
        })