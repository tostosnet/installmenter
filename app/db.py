from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_item(item, db):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


def deeprow2dict(deep_row):
    d = {}
    for item in deep_row:
        if item[0] in d:
            d[item[0]].append(item[1])
            continue
        d[item[0]] = [item[1]]
    return d


# from MySQLdb import Connect, Error
# import time
# "mysql://root:@localhost:3306/demodb"

# while True:
#     try:
#         # mysql db connection
#         conn = Connect(host='localhost', passwd='', user='root', db='tostos')
#     except Error as e:
#         print('Server Connection failed:', e)
#         print('Retrying connection...')
#         time.sleep(2)
#     else:
#         print('Database Connection was successfull!')
#         cur = conn.cursor()
#         cur.execute('use installmenterdb')
#         break

