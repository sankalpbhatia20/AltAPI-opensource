from pydantic import BaseModel, EmailStr
from typing import Optional

#from models import User
class UserInput(BaseModel): # Schema Validation
    asset: str
    date: str
    compound_positivity_score: float
    compound_sentiment: float
    top_url: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel): # The response the user will get after he has signed up
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    