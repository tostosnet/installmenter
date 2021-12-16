from ecdsa.ecdsa import Signature
from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base


class ManagerDB(Base):
    __tablename__ = 'managers'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(length=30), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    surname = Column(String(length=30), nullable=False)
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30))
    phone_number = Column(String(length=15))
    street = Column(String(length=30))
    city = Column(String(length=15))
    state = Column(String(length=15))
    photo = Column(String(length=30))
    created_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)



class ClientDB(Base):
    __tablename__ = 'clients'

    id = Column(String(length=8), primary_key=True, nullable=False)
    surname = Column(String(length=30), nullable=False)
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=30))
    phone_number = Column(String(length=15), nullable=False)
    phone_number_2 = Column(String(length=15))
    email = Column(String(length=30), nullable=False, unique=True)
    password = Column(String(length=64))
    street = Column(String(length=30), nullable=False)
    city = Column(String(length=15), nullable=False)
    state = Column(String(length=15), nullable=False)
    photo = Column(String(length=30), nullable=False)
    id_type = Column(String(length=20), nullable=False)
    id_number = Column(String(length=30), nullable=False, unique=True)
    id_issue_date = Column(Date, nullable=False)
    id_expiry_date = Column(Date)
    id_photo = Column(String(length=30))
    signature_photo = Column(String(length=30))
    form_photo = Column(String(length=30))
    created_date = Column(TIMESTAMP(timezone=True),
                          server_default=text('now()'), nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.id"), nullable=False)



class GuarantorDB(Base):
    __tablename__ = 'guarantors'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    surname = Column(String(length=20), nullable=False)
    first_name = Column(String(length=20), nullable=False)
    last_name = Column(String(length=20))
    phone_number = Column(String(length=15), nullable=False)
    phone_number_2 = Column(String(length=15))
    email = Column(String(length=30), nullable=False, unique=True)
    street = Column(String(length=30), nullable=False)
    city = Column(String(length=15), nullable=False)
    state = Column(String(length=15), nullable=False)
    photo = Column(String(length=30), nullable=False)
    id_type = Column(String(length=20), nullable=False)
    id_number = Column(String(length=30), nullable=False, unique=True)
    id_issue_date = Column(Date, nullable=False)
    id_expiry_date = Column(Date)
    id_photo = Column(String(length=30))
    signature_photo = Column(String(length=30))
    form_photo = Column(String(length=30))
    client_id = Column(String(length=8), ForeignKey(
        "clients.id", ondelete="CASCADE"), nullable=False)
    created_date = Column(TIMESTAMP(timezone=True),
                          server_default=text('now()'), nullable=False)



class ProductDB(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(length=30), nullable=False)
    cat = Column(String(length=15), nullable=False)
    make = Column(String(length=15), nullable=False)
    model = Column(String(length=15), nullable=False)
    color = Column(String(length=15), nullable=False)
    condition = Column(String(length=5), nullable=False)
    photo = Column(String(length=30), nullable=False)
    vin = Column(String(length=17), nullable=False, unique=True)
    plate_num = Column(String(length=10), nullable=False, unique=True)
    installment_price = Column(Integer, nullable=False)
    repayment_price = Column(Integer, nullable=False)
    repayment_rate = Column(String(length=10), nullable=False)
    free_days = Column(String(length=30), nullable=False)
    modified_date = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), onupdate=text('now()'), nullable=False)
    


class OrderDB(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    client_id = Column(String(length=8), ForeignKey("clients.id",
        ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id",
        ondelete="CASCADE"), nullable=False)
    order_date = Column(Date, server_default=text('now()'), nullable=False)
    npayment = Column(Integer, nullable=False)
    last_paid = Column(TIMESTAMP(timezone=True),
                           server_default=text('now()'), onupdate=text('now()'), nullable=False)
    
    
class PaymentDB(Base):
    __tablename__ = 'payments'

    id = Column(String(length=12), primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    total_paid = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    date = Column(Date, server_default=text('now()'), nullable=False)
    time = Column(Time, server_default=text('now()'), nullable=False)
    


class PostDB(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(length=20), nullable=False)
    content = Column(String(length=30), nullable=False)
    published = Column(Boolean, server_default=text("True"), nullable=False)
    owner_id = Column(Integer, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True),
                          server_default=text('now()'), nullable=False)
    