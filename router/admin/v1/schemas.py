from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List



class Country(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class State(BaseModel):
    id: int
    name: str
    country: Country

    class Config:
        from_attributes = True


class City(BaseModel):
    id: int
    name: str
    state: State

    class Config:
        from_attributes = True


class Useradd(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    email: EmailStr = Field(..., max_length=100)
    dob: date
    password: str = Field(..., min_length=4, max_length=50)
    city_id: int = Field(...,  ge=1)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    dob: date
    city_id: int = Field(..., ge=1)


class User(BaseModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: EmailStr
    dob: date
    cities: City

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


class CountryAdd(BaseModel):
    name: str = Field(...,min_length=1, max_length=100)


class StateAdd(BaseModel):
    name: str = Field(...,min_length=1, max_length=100)
    country_id: int


class CityAdd(BaseModel):
    name: str = Field(...,min_length=1, max_length=100)
    state_id: int



class CountryList(BaseModel):
    count: int
    data: List[Country] = []

    class Config:
        from_attributes = True


class StateList(BaseModel):
    count: int
    data: List[State] = []

    class Config:
        from_attributes = True


class CityList(BaseModel):
    count: int
    data: List[City] = []

    class config:
        from_attributes = True