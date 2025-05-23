from fastapi import FastAPI, HTTPException, Depends
from db import SessionLocal, get_or_create_user, authenticate_user, save_search, get_recent_searches, clear_searches
from dotenv import load_dotenv
from pydantic import BaseModel
import requests, os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

class WeatherQuery(BaseModel):
    city: str
    username: str

@app.get("/")
def root():
    return {"message": "FastAPI backend for Weather App is running."}

@app.post("/register")
def register(user: UserLogin):
    db = SessionLocal()
    created = get_or_create_user(db, user.username, user.password)
    return {"message": "User created", "user_id": created.id}

@app.post("/login")
def login(user: UserLogin):
    db = SessionLocal()
    verified = authenticate_user(db, user.username, user.password)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/weather")
def get_weather(city: str, username: str):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": city}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    db = SessionLocal()
    save_search(db, username, city)

    return response.json()

@app.get("/searches")
def get_searches(username: str):
    db = SessionLocal()
    return {"recent_searches": get_recent_searches(db, username)}

@app.delete("/searches")
def delete_searches(username: str):
    db = SessionLocal()
    clear_searches(db, username)
    return {"message": "Search history cleared"}
