import json

from fastapi import FastAPI

app = FastAPI()


def load_data(path=None):

    if path == None:
        return {"error": "file can't be loaded", "why": "path is not correct"}

    with open(path, "r") as file:
        data = json.load(file)

    return data


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
        return users[user_id]

    return {"error": f"no such {user_id} is present"}
