import datetime
from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime.datetime
    
class LoginIn(BaseModel):
    email: EmailStr
    password: str
    
class LoginOut(BaseModel):
    access_token: str
    token_type: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    profile_picture: str | None = None
    created_at: datetime.datetime

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
