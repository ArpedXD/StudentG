from pydantic import BaseModel

class login_information(BaseModel):
    username : str
    password : str