from dependencies.CursorTools import CursorTools
from fastapi import HTTPException

class GroupDB:
    def __init__(self, request):
        self.cursor = CursorTools(request)

    def session_id_user_id(self, session_id):
        self.cursor.execute("SELECT user_id FROM sessions WHERE session_id = %s", (session_id,))
        user_id = self.cursor.fetchone()
        return user_id[0]

    def get_user(self,text):
        self.cursor.execute("SELECT username, user_id FROM users WHERE username LIKE %s", (text,))
        usernames = self.cursor.fetchall()
        self.cursor.close()
        return usernames

    def get_user_id_from_group(self, group_id):
        self.cursor.execute("SELECT user_id FROM group_members WHERE group_id = %s", (group_id,))
        users = self.cursor.fetchall()

        return users

    def get_usernames_from_id(self, user_id):
        self.cursor.execute("SELECT username, user_id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def checkAdmin(self, group_id, user_id):
        self.cursor.execute("SELECT user_role FROM group_members WHERE user_id = %s AND group_id = %s", (user_id, group_id))
        response = self.cursor.fetchone()

        self.cursor.close()
        return response[0]

    def InviteUser(self, group_id,action="None", user_id="None",target_user="None",):
        if action == "Role":
            self.cursor.execute("SELECT user_role FROM group_members WHERE user_id = %s AND group_id = %s", (user_id, group_id))
            return self.cursor.fetchone()[0]

        if action == "isHere":
            self.cursor.execute("SELECT user_id FROM group_members WHERE group_id = %s", (group_id,))
            return self.cursor.fetchall()

        self.cursor.execute("INSERT INTO group_members(group_id, user_id, user_role) VALUES (%s,%s,%s)", (group_id, target_user, "Member"))
        self.cursor.commit()
        self.cursor.close()
        return "Success"

    def removeUser(self, group_id, target_user):
        self.cursor.execute("DELETE FROM group_members WHERE user_id = %s AND group_id = %s", (target_user, group_id))
        self.cursor.commit()
        return 