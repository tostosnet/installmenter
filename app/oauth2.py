from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, db, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
#Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        
        role: str = payload.get("role")
        expire: datetime = payload.get("exp")
        token_data = schemas.TokenData(id=id, role=role, expire=expire)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    if token.role == 'manager': db_table = models.ManagerDB 
    elif token.role == 'client': db_table = models.ClientDB
    else: raise credentials_exception
    
    current_user = db.query(db_table).filter(db_table.id == token.id).first()
    if not current_user:
        raise credentials_exception
    
    return current_user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
