from uuid import UUID, uuid4
from pydantic import BaseModel
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
