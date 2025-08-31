import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List,Any
import json
app = FastAPI(title="microservice")

class User(BaseModel):
    id: int
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
    return max(user.id+1 for user in users)

@app.post('/users', response_model=User)
async def create_user(user: User):
    users = load_users()
    user.id = get_next_id(users)
    users.append(user)
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
async def update_user(user_id: int, updated_user: User):
    users = load_users()
    for idx, user in enumerate(users):
        if user.id == user_id:
            updated_user.id = user_id
            users[idx] = updated_user
            save_users(users)
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete('/users/{user_id}', response_model=User)
async def delete_user(user_id: int):
    users = load_users()
    for user in users:
        if user.id == user_id:
            users.remove(user)
            save_users(users)
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    if not os.path.exists(DATA_FILE):
        os.makedirs(DATA_FILE)



