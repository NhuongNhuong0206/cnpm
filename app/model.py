from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app, login
from flask_login import UserMixin
import enum
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    # active = Column(Boolean, default=True)


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    passw1 = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    address = Column(String(100))
    identification = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    nationality = Column(String(50), nullable=False)
    birthdate = Column(DateTime)

    def __str__(self):
        return self.name







################################# DATABASE PRỌECT #####################3

class Airport(BaseModel):
    __tablename__ = 'airport'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    fl_route1 = relationship('Flight_route', backref='airport', lazy=False)  # 3
    # fl_route2 = relationship('Flight_route', backref='airport', lazy=False)  # 4

    def __str__(self):
        return self.name


# Ma thoi gian dung
class Usage_time(BaseModel):
    __tablename__ = 'usage_time'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    max_time = Column(Integer, nullable=False)
    fl_regulations = relationship('Flight_regulations', backref='usage_time', lazy=False)  # 1

    def __str__(self):
        return self.name


# Database qui dinh chuyen bay
class Flight_regulations(BaseModel):
    __tablename__ = 'flight_regulations'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    usage_time_id = Column(Integer, ForeignKey(Usage_time.id))  # 1
    min_onl_ticket_booking_time = Column(Integer, nullable=False)
    min_ticket_sale_time = Column(Integer, nullable=False)
    min_flight_time = Column(Integer, nullable=False)
    fli = relationship('Flight', backref='flight_regulations', lazy=False)  # 2

    def __str__(self):
        return self.name


# Data base chuyen bay
class Flight(BaseModel):
    __tablename__ = 'flight'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    flight_regulations_id = Column(Integer, ForeignKey(Flight_regulations.id))  # 2
    name_flight = Column(String(50), nullable=False)
    number_empty_seats = Column(Integer, nullable=False)
    number_empty_books = Column(Integer, nullable=False)  # Thuộc tính suy diễn !


    # database tuyen bay
class Flight_route(BaseModel):
    __tablename__ = 'flight_route'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_airport_id = Column(Integer, ForeignKey(Airport.id))  # 3
    # arrival_airport_id = Column(Integer, ForeignKey(Airport.id))  # 4
    name_flight_route = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


# Database lich bay
class Flight_schedule(BaseModel):
    __tablename__ = 'flight_schedule'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    note = Column(String(50))

    def __str__(self):
        return self.name




# Viết bên index nó không hiểu. Phải viết qua model nó mới hiểu
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# @login.user_loader
# def load_user(user_id):
#     return dao.get_user_by_id(user_id)

#########################################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        #
        # u = User(name='admin',
        #          passw1=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN,
        #          address='Tp.HoChiMinh',
        #          identification='ga',
        #          email='abcd@gmail.com',
        #          nationality='VietNam' )
        # db.session.add(u)
        # db.session.commit()



        # a1 = Airport(name='Tan Son Nhat')
        # a2 = Airport(name="Nội Bài")
        # a3 = Airport(name="Côn Đảo")
        # a4 = Airport(name="Cà Mau")
        # a5 = Airport(name="Cần Thơ")
        # a6 = Airport(name="Phú Bài")
        # a7 = Airport(name="Vân Đồn")
        # a8 = Airport(name="Đà Nẵng")
        # a9 = Airport(name="Phú Quốc")
        # a10 = Airport(name="Vinh")
        # q = Flight_regulations(min_onl_ticket_booking_time = 30 ,  min_ticket_sale_time = 90,  min_flight_time = 40 )
        #  q1 = Flight_regulations(min_onl_ticket_booking_time = 50 ,  min_ticket_sale_time = 70,  min_flight_time = 60 )
        #
        #
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        # db.session.add_all([a1, a2])
        #  db.session.add(q1)
        #  db.session.commit()
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])

