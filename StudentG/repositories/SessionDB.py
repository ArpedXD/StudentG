from fastapi import Response, HTTPException
from dependencies.CursorTools import CursorTools
import secrets
import json

class SessionDB:
    def __init__(self, request):
        self.db = CursorTools(request)

    def CreateSession(self, username):
        ValueToReturn = json.dumps({"loggedin" : True, "message" : "Success!"})
        response = Response(content=ValueToReturn) # To json

        session_id = secrets.token_hex(32)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,
            samesite="none"
        )
        
        # take user_id -> insert session_id -> save -> return
        print(username)
        self.db.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        user_id = self.db.fetchone()
        self.db.execute("INSERT INTO sessions(user_id, session_id) VALUES (%s, %s)", (user_id[0], session_id))
        self.db.commit()
        return response
    
    def verifySession(self, session_id):
        self.db.execute("SELECT session_id FROM sessions WHERE session_id = %s", (session_id,))
        if self.db.fetchone() is None:
            self.db.close()
            raise HTTPException(401)
        else:
            self.db.close()
            return