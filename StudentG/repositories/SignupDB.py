from dependencies.CursorTools import CursorTools
import bcrypt

class SignupDB:
    def __init__(self, request):
        self.cursor = CursorTools(request)
    
    def usernameExist(self, username):
        self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        value = self.cursor.fetchone()
        return value
    
    def emailExist(self, email):
        self.cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        value = self.cursor.fetchone()
        print(value)
        return value
    
    def createAccount(self, username, password, email):
        passBytes = password.encode('utf-8') # Convert string to bytes
        salt = bcrypt.gensalt(10)
        hashpassword = bcrypt.hashpw(passBytes, salt)
        self.cursor.execute("INSERT INTO users(username, password, email) VALUES (%s, %s, %s, %s)", (username, hashpassword, email, 0))
        self.cursor.commit()
        return