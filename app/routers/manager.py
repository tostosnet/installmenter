from typing import List
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm.session import Session
from random import randint

from .. import models, schemas, utils, oauth2, db


router = APIRouter(
    prefix="/manager",
    tags=["managers"]
)



def generate_client_id(db: Session, current_user: schemas.User):
    # manager_id + client id from random number
    data = db.query(models.ClientDB.id).filter(models.ClientDB.manager_id == current_user.id).all()
    ids = [row[0] for row in data]
    
    while True:
        num = randint(1000, 9999)
        id = str(current_user.id)+str(num)
        if id not in ids:
            return id



# CREATE MANAGER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MngCreateResponse)
def create_manager(manager: schemas.MngCreate, db_: Session = Depends(db.get_db)):
    '''Create or register new manager'''
    hashed_password = utils.hash_password(manager.password)
    manager.password = hashed_password

    new_manager = models.ManagerDB(**manager.__dict__)
    
    return db.add_item(new_manager, db_)


# CREATE CLIENT
@router.post("/client", status_code=status.HTTP_201_CREATED)
def create_client(
    client: schemas.ClientCreate,
    db_: Session = Depends(db.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)):
    '''Create or register new client'''
    
    client.id = generate_client_id(db_, current_user)
    client.manager_id = current_user.id
    
    client_dict = client.__dict__
    grts = [client_dict.pop(grt) for grt in ['grt1', 'grt2']]
    
    new_client = models.ClientDB(**client_dict)
    new_client = db.add_item(new_client, db_)
    new_client_dict = db.row2dict(new_client)
    
    grt_list = []
    for grt in grts:
        if grt:
            grt.client_id = client.id
            grt = schemas.GuarantorCreate(**grt.__dict__)
            grt = models.GuarantorDB(**grt.__dict__)
            grt_list.append(db.add_item(grt, db_))
            
    new_client = schemas.ClientCreateResponse(
        **new_client_dict, guarantors=grt_list)

    return new_client


# GET ONE CLIENT
@router.get("/client/{id}", response_model=schemas.ClientGetResponse)
def get_client(id: str, db: Session = Depends(db.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    client = db.query(models.ClientDB).filter(
        models.ClientDB.manager_id == current_user.id, models.ClientDB.id == id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Client with ID {id} Not Exist')
    return client


# GET ALL CLIENTS
@router.get('/client')
def get_clients(db_: Session = Depends(db.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    clients = db_.query(models.ClientDB, models.GuarantorDB).join(models.GuarantorDB, models.GuarantorDB.client_id == models.ClientDB.id, isouter=True).filter(models.ClientDB.manager_id == current_user.id).all()
    
    clients_dict = db.deeprow2dict(clients)

    clients = [schemas.ClientGetResponse(**client.__dict__, guarantors=clients_dict[client] if clients_dict[client][0] else []) for client in clients_dict]
    
    return clients


# GET ONE GUARANTOR
@router.get("/grt/{id}", response_model=List[schemas.GrtGetResponse])
def get_grt(id: str, db: Session = Depends(db.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    db_table_col = models.GuarantorDB.client_id if len(id) > 4 else models.GuarantorDB.id
    
    grts = db.query(models.GuarantorDB).filter(db_table_col == id).all()
    if not grts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Guarantor does not exist')
    
    if grts[0].client_id[:-4] != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid request')
    
    return grts


# GET ALL GUARANTOR
@router.get('/grt', response_model=List[schemas.GrtGetResponse])
def get_grts(db: Session = Depends(db.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    grts = db.query(models.GuarantorDB).filter(
        models.GuarantorDB.client_id.like(str(current_user.id)+'%')).all()
    
    if not grts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No content in the database')

    return grts

