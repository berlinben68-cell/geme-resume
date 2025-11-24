import os
import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# In a real app, use a database session
# from app.db import get_db

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "mock_id")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "mock_secret")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str

@router.get("/login/github")
def login_github():
    """
    1. Redirect the user to GitHub to authorize permissions.
    """
    scope = "read:user repo"
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope={scope}"
    return RedirectResponse(url=github_auth_url)

@router.get("/login/github/callback")
def github_callback(code: str):
    """
    2. Handle the callback and exchange the code for an Access Token.
    3. Store the encrypted Access Token securely (Mocked here).
    """
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }
    
    # Exchange code for token
    response = requests.post(token_url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")
        
    token_data = response.json()
    
    if "error" in token_data:
         raise HTTPException(status_code=400, detail=token_data["error_description"])
         
    access_token = token_data["access_token"]
    
    # TODO: Encrypt and store access_token in DB linked to user
    # save_token_to_db(access_token)
    
    return {"message": "Login successful", "access_token": "REDACTED_FOR_SECURITY"}
