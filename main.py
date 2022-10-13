from http.client import HTTPException
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI
from models import Gender, PostModel, User,Role, UserUpdate

app = FastAPI()
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



