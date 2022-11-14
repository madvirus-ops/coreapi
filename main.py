# from http.client import HTTPException

from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Query, Path,Cookie
from models import *
from authentication import *
from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save
from typing import List,Optional,Type
from tortoise import BaseDBAsyncClient 

app = FastAPI()

@post_save(UserModel)
async def create_business(
    sender: "Type[UserModel]", 
    instance: UserModel, 
    created: bool, 
    using_db: "Optional[BaseDBAsyncClient]", 
    update_field: List[str]
    ) -> None:

    if created:
        business_obj = await BusinessModel.create(
            business_name = instance.username,owner = instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
        #fuck 



register_tortoise(
    app,
    db_url ="sqlite://database.sqlite3",
    modules = {"models":["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


db: List[User] = [
    User(
        id=uuid4(),
        first_name="john",
        last_name="doe",
        gender=Gender.female,
        roles=Role.student
        ),
        User(
        id=uuid4(),
        first_name="john",
        last_name="beans",
        gender=Gender.male,
        roles=Role.admin
        ),
]
pdb: List[PostModel] = [ PostModel(
    id=uuid4(),
    title="post 1",
    body = "post one djdoi doifn foidf dfoimfd foifme ",
    slug = "slug-log",
    author ="josh",
) 
]

#fastapi course from that java guy
@app.get("/")
async def root():
    return {"hello":"world"}

@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def create_user(user:User):
    if user in db:
        return {"error":"user exists"}
    else:
        db.append(user)
        return {"created":"user created","id":user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"deleted":"deleted"}
    raise HTTPException(
        status_code=404,
        detail = f"user with {user_id} does not exist"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update:UserUpdate,user_id:UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            status = {
                "code":200,
                "detail" : f"user with {user_id} has been updated"
            }
            return status
        status = {
                "code":404,
                "detail" : f"user with {user_id} does not exist"
            }
        return status 


# to create post
@app.post("/api/post/")
async def create_post(post:PostModel):
    if post in pdb:
        status = {
            "code":400,
            "detail ":f" {post.title} already exists"
        }
        return status
    else:
        pdb.append(post)
        status = {
            "code":201,
            "detail ":f" {post.title} has been created succesfully"
        }
        return status


@app.get("/api/post/")
async def get_post():
    return pdb 
# e commerce fastapi tut
@app.post("/api/register")
async def register_user(user: usermodel_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info['password'])
    user_obj = await UserModel.create(**user_info)
    new_user = await usermodel_pydantic.from_tortoise_orm(user_obj)
    return {
        "status":"ok",
        "data":f"hello {new_user.username}, thanks for choosing shit"
    }



#fastapi crash course
#query parameters takes ?id=id
@app.get("/post/")
async def get_post_by_id(id:int | None =None):
    if id and  id in pdb:
        return pdb.__getitem__(id)
    return pdb

#url and path parameters 
@app.get("/users/{user_id}/items/{items_id}")
async def get_post_by_user_id(user_id:str, items_id:str,q:str | None = None ):
    item = {"item_id":items_id,"user_id":user_id}
    if q:
        item = {"item_id":items_id,"user_id":user_id,"q":q}
        return item
    return item

summary = "query parameters are passed in the function, while path parameters are passed in the path/urls"


#request body
@app.post("/items")
def create_item(item: Itemss):
    item_dict = item.dict()
    if item.tax:
        price_tax = item.price + item.tax
        item_dict.update({"price_tax":price_tax})

    return item_dict

@app.put("/items/{id}")
async def create_put(id:int,item:Itemss):
    return {"item_id":id,**Itemss.dict()}


# @app.get("/item")
# async def search_item(id:str | None=None ):
#     return {"true":id}
# def TrainModel():
#     list_update = {

#     }
#     for x in range(10):
#         list_update[x] = x



@app.get("/item",description="this endponit fuck you up.. ")
async def reset_items(q: str | None = Query(None)):
    results = {"item":q}
    return results

@app.get("/item_val/{id}",description="this also")
async def validate_item(id:int,q:str | None=Query(None)):
    results = {"item_id":id}
    if q:
        results.update({"q":q})         
    return results



#cookie
@app.get("/cookie")
async def get_cookie(cookie_id:str | None=Cookie(None)):
    return {"cookie_id":cookie_id}