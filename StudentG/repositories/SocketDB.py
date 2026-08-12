from dependencies.CursorTools import CursorTools

class SocketDB:
    def __init__(self, socket, session_id):
        self.cursor = CursorTools(socket)
        self.cursor.execute("SELECT user_id FROM sessions WHERE session_id = %s", (session_id,))
        self.user_id = self.cursor.fetchone()
        self.cursor.execute("SELECT username FROM users WHERE user_id = %s", (self.user_id[0],))
        self.username = self.cursor.fetchone()

    def GetGroups(self):
        user_id = self.user_id[0]
        self.cursor.execute("SELECT group_id FROM group_members WHERE user_id = %s", (user_id,))
        gGroup = self.cursor.fetchall()
        return [item for my_tuple in gGroup for item in my_tuple]

    def Save_Message(self, chat, group):
        user_id = self.user_id[0]
        self.cursor.execute("INSERT INTO group_messages(group_id,message,user_id) VALUES (%s,%s,%s)",(group, chat, user_id))
        self.cursor.commit()
        return