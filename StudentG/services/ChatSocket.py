from repositories.SocketDB import SocketDB
from fastapi import WebSocketDisconnect
import json
class WebsocketRepo:
    async def Websocket(websocket, chat, session_id, activeUsers):
        socketManager = SocketDB(websocket, session_id)
        await websocket.accept()
        try:
            while True:
                for group_id in socketManager.GetGroups(): # Handles Group Pulling
                    if group_id not in activeUsers:
                        activeUsers[group_id] = {}

                    if session_id not in activeUsers[group_id]: 
                        activeUsers[group_id][session_id] = websocket

                message = await websocket.receive_text()
                print(message)
                for ChatGroup in activeUsers:
                    if chat == "": break
                    if ChatGroup == int(chat):
                        for key in activeUsers[int(chat)].values():
                            if websocket != key:
                                await key.send_text(json.dumps({
                                    "username":socketManager.username[0],
                                    "message" : message,
                                    "id":5
                                }))
                            else:
                                socketManager.Save_Message(message, int(chat))
        except WebSocketDisconnect:
            socketManager.cursor.close()
            try:
                for group_id in list(activeUsers.keys()): # Handles Group Removal
                    if session_id in activeUsers[group_id]: 
                        activeUsers[group_id].pop(session_id)
                        if not activeUsers[group_id]:
                            activeUsers.pop(group_id) 
            finally:
                pass