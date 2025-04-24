from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Allow React frontend to connect (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class User(BaseModel):
    email: str
    password: str

# Create or connect to SQLite database
def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")
    return conn

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

# Signup endpoint
@app.post("/signup")
async def signup(user: User):
    conn = get_db()
    try:
        conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, user.password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "Signup successful"}

# Login endpoint
@app.post("/login")
async def login(user: User):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (user.email, user.password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
