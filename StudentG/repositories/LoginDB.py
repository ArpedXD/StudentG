from dependencies.CursorTools import CursorTools
import bcrypt

class LoginDB:
    def __init__(self,request):
        self.cursor = CursorTools(request)

    def Login(self, username, password):
        self.cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        user_id = self.cursor.fetchone()

        if user_id is None:
            return [False, {"loggedin": False, "message" : "Account Does Not Exist"}]
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        passwordHash = self.cursor.fetchone()

        if bcrypt.checkpw(password.encode('utf-8'), passwordHash[0].encode('utf-8')):
            return [True, {"loggedin": True, "message" : "Correct Password"}]
        else:
            return [False, {"loggedin": False, "message" : "Wrong Password"}]