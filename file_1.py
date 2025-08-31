import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List,Any
import json
app = FastAPI(title="microservice")

class User(BaseModel):
    name: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False


DATA_FILE = 'users_data.json'

def load_users() -> List[User]: #read json db with users info and load as list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return [User(**user) for user in json.load(file)]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
    else:
        return []


def save_users(users: List[User]) -> None: #save/create json with user info
    with open(DATA_FILE, 'w') as file:
        users_data = [user.model_dump() for user in users]
        json.dump(users_data, file, indent=2)

def get_next_id(users: List[User]) -> int:
    if not users:
        return 0
    return max(user.id + 1 for user in users)

@app.post('/users', response_model=User)
async def create_user(user: User):
    users = load_users()
    users.id = get_next_id(users)
    user.append(user)
    save_users(users)
    return user

@app.get('/users', response_model=List[User])
async def get_users():
    return load_users()

@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int) -> User:
    users = load_users()
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user: User):
    users = load_users()
    for user in users:
        if user.id == user_id:
            user.name = user.name
            return user
