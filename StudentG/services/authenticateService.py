from core.Validators import Validator
from repositories.SignupDB import SignupDB
from repositories.LoginDB import LoginDB
from repositories.SessionDB import SessionDB
from core.Enumerators import AuthType

class authenticateService:
    def signupservice(request, signup, session):
        signupVAL = Validator(
            signup.username, 
            signup.password, 
            AuthType.SIGNUP,
            signup.confirmPassword, 
            signup.email
        )
        signupDB = SignupDB(request)

        RequirementsMet = signupVAL.confirmRequirements()
        
        if not RequirementsMet[0]:
            return RequirementsMet[1]

        if signupDB.usernameExist(signup.username) is not None:
            signupDB.cursor.close()
            return {"loggedin": False, "message": "Username already Exists"}
        
        if signupDB.emailExist(signup.email) is not None:
            signupDB.cursor.close()
            return {"loggedin": False, "message": "Mail Already Used"}
        
        signupDB.createAccount(signup.username, signup.password, signup.email) 
        sessiondb = SessionDB(request)

        valuetoreturn = sessiondb.CreateSession(signup.username)
        signupDB.cursor.close() # Close when done using DB validation
        return valuetoreturn
    
    def loginservice(request, login, session):
        loginVal = Validator(
            login.username, 
            login.password,
            AuthType.LOGIN
        )
        
        RequirementsMet = loginVal.confirmRequirements()

        if not RequirementsMet[0]:
            return RequirementsMet[1]
        
        loginDB = LoginDB(request)
        LoggingIn = loginDB.Login(
            login.username, 
            login.password
        )

        if LoggingIn[0]:
            sessiondb = SessionDB(request)
            valuetoreturn = sessiondb.CreateSession(login.username)

            loginDB.cursor.close()
            return valuetoreturn
        else:
            loginDB.cursor.close()
            return LoggingIn[1]