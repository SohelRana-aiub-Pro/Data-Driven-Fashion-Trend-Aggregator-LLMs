# app/models.py
from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    style_pref: str
    budget: int
    occasion: str


#