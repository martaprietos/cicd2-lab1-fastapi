from fastapi import FastAPI, status, HTTPException
from app.schemas import UserCreate

app = FastAPI(title="Lab 1 - FastAPI User API")

users: list[UserCreate] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
   for existing_user in users:
      if existing_user.user_id == new_user.user_id:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this user_id already exists",
        )
   users.append(new_user)
   return new_user

@app.get("/api/users")
def get_users():
   return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
   for existing_user in users:
      if existing_user.user_id == user_id:
         return existing_user
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="User not found",
        )