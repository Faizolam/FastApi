from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils,oauth2

# Tag for categorize
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
# def login(user_credntials: schemas.UserLogin = Depends(), db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm will retrive credentials username and password, and store in user_credentials and it can be email or username anything but you have to pass field "user_credentials.username".
    # user=db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user=db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Creadentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create a token
    #return token
    #In payload you can give whatever you want like user_role, the scope of different endpoints or anything else but here i'm giving user_id
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}