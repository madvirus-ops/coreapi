from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI
from models import Gender, User,Role

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
        return {"created":"user created"}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return

