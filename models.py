from uuid import UUID, uuid4
from pydantic import BaseModel,create_model
from typing import List, Optional
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    student = "student"
    user = "user"



class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name:str
    last_name:str
    middle_name:Optional[str]
    gender: Gender
    roles: Role

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name:Optional[str]
    roles:Optional[Role]

class PostModel(BaseModel):
    id: Optional[UUID] = uuid4()
    title:str
    slug:Optional[str]
    body:str
    # image:[str]
    author:str


