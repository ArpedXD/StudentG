from dependencies.CursorTools import CursorTools
import random
import string

class ChatDB:
    def __init__(self, request, session_id):
        self.cursor = CursorTools(request)
        self.cursor.execute("SELECT user_id FROM sessions WHERE session_id = %s", (session_id,))
        self.user_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT username FROM users WHERE user_id = %s", (self.user_id,))
        self.username = self.cursor.fetchone()

        self.InviteLength = 10

    def GroupExist(self, group_name):
        self.cursor.execute("SELECT group_name FROM group_chat WHERE group_name = %s", (group_name.group_name,))
        res = self.cursor.fetchone()
        if res is None:
            return None
        return res[0]

    def get_group_limit(self):
        self.cursor.execute("SELECT group_limit FROM users WHERE user_id = %s", (self.user_id,))
        return self.cursor.fetchone()[0]

    def create_chat(self, group_chat):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=self.InviteLength))
        self.cursor.execute("INSERT INTO group_chat(group_name, group_code) VALUES (%s, %s)", (group_chat.group_name, code)) # Creates group chat

        self.cursor.execute("SELECT group_id FROM group_chat WHERE group_name = %s", (group_chat.group_name,))
        group_id = self.cursor.fetchone()

        self.cursor.execute("INSERT INTO group_members(group_id, user_id, user_role) VALUES (%s, %s, %s)", (group_id[0], self.user_id, "Admin"))
        self.cursor.commit()
        return

    def getGchats(self):
        self.cursor.execute("SELECT group_id FROM group_members WHERE user_id = %s", (self.user_id,))

        all_chats = []
        for group_id in self.cursor.fetchall():
            self.cursor.execute("SELECT group_name, group_id FROM group_chat WHERE group_id = %s", (group_id[0],))
            all_chats.append(self.cursor.fetchall()[0])
        return all_chats

    def load_messages(self, group_id, messages, before):
        if before != None:
            self.cursor.execute("SELECT message, user_id, message_id FROM group_messages WHERE group_id = %s AND message_id < %s ORDER BY message_id DESC LIMIT %s", (group_id,before, messages))
        else:
            self.cursor.execute("SELECT message, user_id, message_id FROM group_messages WHERE group_id = %s ORDER BY message_id DESC LIMIT %s", (group_id, messages))
        raw_messages = []
        for each in self.cursor.fetchall():
            self.cursor.execute("SELECT username FROM users WHERE user_id = %s", (each[1],))
            values = self.cursor.fetchone()
            raw_messages.append({
                "username": values[0],
                "message": each[0],
                "id": each[2]
            })
        return raw_messages