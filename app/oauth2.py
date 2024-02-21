from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expriation tiome

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()

    #expire time
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # create jwt tocken
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


#Verify access tocken to give and take data
def verify_access_tocken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("user_id")
        id_str = str(id)
        print(type(id_str))
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id_str)
    except JWTError:
        raise credentials_exception
    return token_data
    
#Take the tocken from request automaticaly extract id for us, it is going to verify access tocken is correct by calling verify_access_tocken, automaticaly fetch the user from the database 
    

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_tocken(token, credentials_exception)

    user=db.query(models.User).filter(models.User.id == token.id).first()

    return user