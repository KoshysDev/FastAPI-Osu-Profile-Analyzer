from typing import List

import fastapi as _fastapi
import fastapi.security as _security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status, Response

import os

import sqlalchemy.orm as _orm

import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

root = os.path.dirname(os.path.abspath(__file__))

@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    #await _services.create_token(user)
    return await _services.create_user(user, db)

@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(
    lead: _schemas.LeadCreate, 
    user: _schemas.User=_fastapi.Depends(_services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    return await _services.create_lead(user=user, db=db, lead=lead)

@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(
    user: _schemas.User=_fastapi.Depends(_services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    return await _services.get_leads(user=user, db=db)

@app.get("/api/leads/{lead_id}", status_code=status.HTTP_200_OK)
async def get_lead(
    lead_id: int,
    user: _schemas.User=_fastapi.Depends(_services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    return await _services.get_lead(lead_id, user, db)

@app.delete("/api/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    user: _schemas.User=_fastapi.Depends(_services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    await _services.delete_lead(lead_id, user, db)
    return {"message", "Deleted Successfully"}

@app.put("/api/leads/{lead_id}", status_code=status.HTTP_200_OK)
async def update_lead(
    lead_id: int,
    lead: _schemas.LeadCreate,
    user: _schemas.User=_fastapi.Depends(_services.get_current_user), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):

    await _services.update_lead(lead_id, lead, user, db)
    return {"message", "Updated Successfully"}

@app.get("/")
async def index():
    with open(os.path.join(root, 'index.html')) as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")
