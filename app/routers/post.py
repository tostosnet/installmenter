from typing import Optional
from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from .. import models, schemas, oauth2
from ..db import add_item, engine, get_db


router = APIRouter(
    prefix="/post",
    tags=["posts"]
)



@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.PostDB).filter(models.PostDB.owner_id == current_user.id).filter(models.PostDB.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.PostDB).filter(
        models.PostDB.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")
    
    return {"title": f'post with id {id}', "data": post}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostModel, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.PostDB(owner_id=current_user.id, **post.__dict__)
    
    return add_item(new_post, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.PostDB).filter(
        models.PostDB.id == id)
    
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {id} Not Exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested action")
    
    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostModel, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.PostDB).filter(
        models.PostDB.id == id)

    db_post = query.first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {id} Not Exist')
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")
        
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return query.first()


