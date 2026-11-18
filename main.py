import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your Next.js app to access the API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Pydantic model matching your JSON fields (excluding 'id', which is auto-generated)
class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "viewer"
    location: str
    status: str = "active"


def load_data(path=None):
    if path is None:
        return {"error": "file can't be loaded", "why": "path is not correct"}

    with open(path, "r") as file:
        data = json.load(file)

    return data


def save_data(data, path="data/users.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


@app.get("/")
def home():
    return {"message": "Hello User"}


@app.get("/about")
def about():
    return {"name": "Allsabah", "app": "Backend App"}


@app.get("/users")
def users():
    return load_data(path="data/users.json")


@app.get("/user/{user_id}")
def user_id(user_id):
    users = load_data(path="data/users.json")

    if str(user_id) in users:
        return users[str(user_id)]

    return {"error": f"no such {user_id} is present"}


# 2. POST route to create a new user
@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    users = load_data(path="data/users.json")

    # Auto-generate the next ID based on existing keys ("1", "2", "3", "4" -> 5)
    if users:
        next_id = max(int(k) for k in users.keys()) + 1
    else:
        next_id = 1

    # Format the new user entry to match your exact JSON structure
    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "location": user.location,
        "status": user.status,
    }

    # Store using string key ("5") and save to users.json
    users[str(next_id)] = new_user
    save_data(users, path="data/users.json")

    return {
        "message": "User created successfully",
        "user": new_user,
    }
