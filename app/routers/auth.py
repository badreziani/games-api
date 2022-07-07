from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import utils, oauth2

from app import models
from .. import database, schemas

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


@router.post('/api/login', response_model=schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.username == credentials.username).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=[{"msg": "Vos identifiants sont incorrects."}])

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=[{"msg": "Vos identifiants sont incorrects."}])
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "fullname": user.fullname, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/api/users/me', response_model=schemas.User)
async def fetch_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    user = oauth2.get_current_user(token=token, db=db)
    return user
