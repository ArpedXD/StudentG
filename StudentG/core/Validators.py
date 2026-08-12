from Exceptions.LoginAndSignupExceptions import passwordLess, usernameLess, PassnotSame, EmptyValues, WrongGmail
from dependencies.CursorTools import CursorTools
from core.Enumerators import AuthType

class Validator:
    def __init__(self, username, password, type, confirmpassword="None", email="None"):
        self.username = username
        self.password = password
        self.confirmpassword = confirmpassword
        self.email = email
        self.type = type

    def confirmRequirements(self):
        list = [self.username,self.password,self.confirmpassword,self.email]
        try:
            for ls in list:
                if ls == "":
                    raise EmptyValues(f"Please Fill in the forms")
            if len(self.username) < 8:
                raise usernameLess("Username is Less than 8")
            if len(self.password) < 8:
                raise passwordLess("Password is Less than 8")
            
            if self.type == AuthType.SIGNUP: # Conditional statement if the type is a SIGNUP
                if self.password != self.confirmpassword:
                    raise PassnotSame("Password is not the same")
                if "@" not in self.email:
                    raise WrongGmail("Please use the correct email!")
                
        except (passwordLess , usernameLess , PassnotSame , EmptyValues, WrongGmail) as e:
            return [False, {"loggedin": False, "message" : str(e)}]
        
        return [True, 0]