from pydantic import BaseModel

class signup_information(BaseModel):
    username : str
    password : str
    email : str
    confirmPassword : str