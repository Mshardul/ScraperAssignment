'''
This module defines the authentication routes for the API.
'''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy in-memory token storage for simplicity
FAKE_TOKEN = "fake-oauth2-token"

class Token(BaseModel):
    ''' This indicates the Login Token passed in the request '''
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    ''' user login endpoint '''
    # OUT_OF_SCOPE: Authenticate user and generate token
    print("router/user/login/form_data: ", form_data)
    return {"access_token": FAKE_TOKEN, "token_type": "bearer"}

def authenticate_token(token: str = Depends(oauth2_scheme)):
    ''' user authentication endpoint '''
    # OUT_OF_SCOPE: Authenticate token sent in the request
    if token != FAKE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
