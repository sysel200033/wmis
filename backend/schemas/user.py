from datetime import date

from pydantic import BaseModel

# User Schema


class Base(BaseModel):
    email: str
    birthday: date
    phone_number: str

class Register(Base):
    password: str


class Password(BaseModel):
    password: str


class Birthday(BaseModel):
    birthday: date
