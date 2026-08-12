from repositories.ChatDB import ChatDB
from Exceptions.ChatExceptions import GROUPALREADYEXISTS, GROUPLIMIT, GROUPNAMETOOLONG
from repositories.SessionDB import SessionDB

class ChatFunctionality:
    def CreateGroupChat(request, group_chat, session_id):
        sessionDB = SessionDB(request)
        sessionDB.verifySession(session_id)  # Verify session first to avoid cursor leak

        chatdb = ChatDB(request, session_id)
        try:
            if chatdb.GroupExist(group_chat) is not None:
                raise GROUPALREADYEXISTS("GROUP ALREADY EXISTS")

            if chatdb.get_group_limit() >= 5:
                raise GROUPLIMIT("GROUP CREATION LIMIT REACHED")

            if len(group_chat.group_name) >= 9:
                raise GROUPNAMETOOLONG("GROUP NAME TOO LONG")
        except (GROUPALREADYEXISTS, GROUPLIMIT, GROUPNAMETOOLONG) as e:
            chatdb.cursor.close()
            return {"Created": False, "Reason": str(e)}

        chatdb.create_chat(group_chat)
        chatdb.cursor.close()
        return {"Created": True, "Reason": "Yay"}

    def GetGroupChat(request, session_id):
        sessionDB = SessionDB(request)
        sessionDB.verifySession(session_id)

        chatdb = ChatDB(request, session_id)
        Group_chats = chatdb.getGchats()
        chatdb.cursor.close()
        return Group_chats

    def load_chats(request, session_id, group_id, messages, before):
        sessionDB = SessionDB(request)
        sessionDB.verifySession(session_id)

        chatDB = ChatDB(request, session_id)
        raw_messages = chatDB.load_messages(group_id, messages, before)
        chatDB.cursor.close()

        # Service-layer presentation logic: mark own messages as "Me"
        formatted_messages = []
        for msg in raw_messages:
            if msg["username"] == chatDB.username[0]:
                formatted_messages.append({
                    "username": "Me",
                    "message": msg["message"],
                    "id": msg["id"]
                })
            else:
                formatted_messages.append(msg)
        return formatted_messages