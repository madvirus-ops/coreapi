from email.policy import default
from operator import index
from uuid import UUID, uuid4
from pydantic import BaseModel
from tortoise import Model , fields
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List, Optional
from enum import Enum, unique
from datetime import datetime


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


#crash course
class Itemss(BaseModel):
    name: str
    price: float
    description: Optional[str]
    tax:Optional[float]



class UserModel(Model):
    id = fields.IntField(pk = True,index = True)
    username = fields.CharField(max_length=25, null = False,unique= True),
    email = fields.CharField(max_length=255,unique=True)
    password = fields.CharField(max_length=100,null= False)
    is_verified = fields.BooleanField(default=False)
    joined_date = fields.DatetimeField(default=datetime.utcnow)

class BusinessModel(Model):
    id = fields.IntField(pk = True,index = True)
    business_name = fields.CharField(max_length=70,unique=True,null=False)
    city = fields.CharField(max_length=70,null=False,default="unspecified")
    region = fields.CharField(max_length=70,null=False,default="unspecified")
    description = fields.CharField(max_length=70,null=False)
    logo = fields.CharField(max_length=70,default="unspecified.jpg",null=False)
    owner = fields.ForeignKeyField(model_name="models.UserModel",related_name="business")


class ProductModel(Model):
    id = fields.IntField(pk = True,index = True)
    name = fields.CharField(max_length=70,null=False,index=True)
    category = fields.CharField(max_length=70,index=True,null=True)
    original_price = fields.DecimalField(max_digits=12,decimal_places=2)
    new_price = fields.DecimalField(max_digits=12,decimal_places=2)
    percentage_discount = fields.IntField()
    expires = fields.DatetimeField(default=datetime.utcnow)
    product_image = fields.CharField(max_length=200,default="unspecified.jpg")
    business = fields.ForeignKeyField(model_name="models.BusinessModel",related_name="products")  


usermodel_pydantic = pydantic_model_creator(UserModel,name="UserModel",exclude=("is_verified",))
usermodel_pydanticIn = pydantic_model_creator(UserModel,name="UserModelIn",exclude_readonly=True,exclude=("is_verified","joined_date"))
usermodel_pydanticOut = pydantic_model_creator(UserModel,name="UserModelOut",exclude=("password",))

business_pydantic = pydantic_model_creator(BusinessModel,name="BusinessModel")
business_pydanticIn = pydantic_model_creator(BusinessModel,name="BusinessModelIn",exclude_readonly=True)

product_pydantic = pydantic_model_creator(ProductModel,name="ProductModel")
product_pydanticIn = pydantic_model_creator(ProductModel,name="ProductModelIn",exclude=("percentage_discount","id",))



