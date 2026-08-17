import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from pydantic import BaseModel

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing from .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="Auth Practice API",
    description="Secure API using FastAPI and Supabase Auth",
    version="1.0.0"
)

# FastAPI HTTPBearer Security Scheme (Stage 5 Swagger Auth Enable karta hai)
security = HTTPBearer()

class AuthRequest(BaseModel):
    email: str
    password: str

# ---------------------------------------------------------
# Reusable Dependency (Stage 4 Guard / Middleware)
# ---------------------------------------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if user_response.user is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ---------------------------------------------------------
# Public Routes (Stage 2 & Root)
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase"}

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# ---------------------------------------------------------
# Auth Routes (Stage 1 & Stage 4 Logout)
# ---------------------------------------------------------
@app.post("/auth/signup", status_code=201)
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    response = supabase.auth.sign_up({"email": data.email, "password": data.password})
    if response.user is None:
        raise HTTPException(status_code=400, detail="Unable to create account")
    
    return {"user": {"id": response.user.id, "email": response.user.email}}

@app.post("/auth/login")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        response = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    if response.session is None:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }

@app.post("/auth/logout", status_code=204)
def logout(auth_data: dict = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
        return
    except Exception:
        raise HTTPException(status_code=401, detail="Logout failed")

# ---------------------------------------------------------
# Protected Routes (Stage 3 & Stage 4)
# ---------------------------------------------------------
@app.get("/protected/profile")
def protected_profile(auth_data: dict = Depends(get_current_user)):
    user = auth_data["user"]
    return {
        "message": "Protected profile",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }

@app.get("/protected/dashboard")
def protected_dashboard(auth_data: dict = Depends(get_current_user)):
    user = auth_data["user"]
    return {
        "message": f"Welcome to dashboard, {user.email}!"
    }