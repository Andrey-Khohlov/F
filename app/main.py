from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import uvicorn
from fastapi import FastAPI, Cookie, Depends, HTTPException, Response, Form, Request, Header, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.models import User, User1, User2, Feedback, UserCreate, SearchProducts, User3
from data.fake_db import sample_products, users_db, user_data




if __name__ == '__main__':
    uvicorn.run(app="app.main:app",
                host='127.0.0.1',
                port=8000,
                reload=True)
