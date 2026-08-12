
from repositories.GroupDB import GroupDB
from fastapi import HTTPException

class GroupService:
    def search_user(request, text):
        searchdb = GroupDB(request)
        text = '%' + text + '%'
        return searchdb.get_user(text)

    def load_members(request, group_id, session_id):
        searchdb = GroupDB(request)
        users = searchdb.get_user_id_from_group(group_id)
        user_id = searchdb.session_id_user_id(session_id)
        usernames = []
        for each in users:
            for value in each:
                username_and_id = searchdb.get_usernames_from_id(value)
                if user_id == username_and_id[0][1]:
                    break; 
                usernames.append(username_and_id[0])
        searchdb.cursor.close()
        return usernames


    def isAdmin(request, group_id,  session_id):
        searchdb = GroupDB(request)
        user_id = searchdb.session_id_user_id(session_id)
        response = searchdb.checkAdmin(group_id, user_id)

        if response == None or response != "Admin":
            return False
        return True

    
    def inviteUser(request, chat, target_user,session_id):
        searchdb = GroupDB(request)
        user_id = searchdb.session_id_user_id(session_id)
        role = searchdb.InviteUser(chat, "Role", user_id)
        if role != "Admin":
            raise HTTPException(403, "NOT AN ADMIN")

        for each in searchdb.InviteUser(chat, "isHere", user_id):
            if target_user == each[0]:
                raise HTTPException(401, "USER IS ALREADY HERE")
        return searchdb.InviteUser(chat, "None", user_id, target_user )
    
    def removeuser(request, chat, target_user, session_id):
        searchdb = GroupDB(request)
        user_id = searchdb.session_id_user_id(session_id)

        role = searchdb.InviteUser(chat, "Role", user_id)
        if role != "Admin":
            raise HTTPException(403, "NOT AN ADMIN")

        searchdb.removeUser(chat, target_user)
        searchdb.cursor.close()
        return "Success!"