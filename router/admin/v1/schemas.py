from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List


class Useradd(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    email: EmailStr = Field(..., max_length=100)
    dob: date
    password: str = Field(..., min_length=4, max_length=50)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    dob: date


class User(BaseModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: EmailStr
    dob: date

    class Config:
        from_attributes = True


class UserList(BaseModel):
    data: List[User]
    count: int

    class Config:
        from_attributes = True


class LoginResponse(User):
    access_token: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=3, max_length=50)


class ForgetPassword(BaseModel):
    email: EmailStr = Field(..., max_length=100)


class ConfirmPassword(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    otp: str = Field(..., min_length=6)
    password: str = Field(..., min_length=3, max_length=50)


class ChangePassword(BaseModel):
    old_password: str = Field(..., min_length=3, max_length=50)
    new_password: str = Field(..., min_length=3, max_length=50)
