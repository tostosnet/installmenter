from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils, db, oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(db.get_db)):
    db_table = models.ManagerDB if user_credentials.role == 'manager' else models.ClientDB
    user = db.query(db_table).filter(db_table.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "role": user_credentials.role})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
