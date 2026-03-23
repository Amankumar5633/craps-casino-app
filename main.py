from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# -------- FAKE DATABASE --------
users = {}

# -------- MODELS --------
class User(BaseModel):
    username: str
    password: str

# -------- REGISTER --------
@app.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User exists")
    
    users[user.username] = {
        "password": user.password,
        "balance": 1000
    }
    return {"msg": "User created"}

# -------- LOGIN --------
@app.post("/login")
def login(user: User):
    if user.username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    if users[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Wrong password")
    
    return {"msg": "Login success", "balance": users[user.username]["balance"]}

# -------- PLAY GAME --------
@app.post("/roll/{username}")
def roll(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    total = d1 + d2

    # simple win/lose
    if total in [7,11]:
        users[username]["balance"] += 100
        result = "win"
    elif total in [2,3,12]:
        users[username]["balance"] -= 100
        result = "lose"
    else:
        result = "point"

    return {
        "dice": [d1, d2],
        "total": total,
        "result": result,
        "balance": users[username]["balance"]
    }