from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app, login_manager
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


# class Client(BaseModel):
#     address = Column(String(100))
#     identification = Column(String(20), unique=True, nullable=True)
#     email = Column(String(50), nullable=False)
#     nationality = Column(String(50))
#     birthdate = Column(DateTime)
#     phone_number = Column(Integer)
class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    passw1 = Column(String(100))
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    address = Column(String(100))
    identification = Column(String(20), unique=True, nullable=True)
    email = Column(String(50), nullable=False)
    nationality = Column(String(50))
    birthdate = Column(DateTime)
    # phone_number = Column(Integer)

    def __str__(self):
        return self.name


#Bảng sân bay
class Airport(BaseModel):
    __tablename__ = 'airport'
    name = Column(String(50), nullable=True)


    def __str__(self):
        return self.name


    # Bảng Tuyến bay
class Flight_route(BaseModel):
    __tablename__ = 'flight_route'
    departure_airport_id = Column(Integer, ForeignKey(Airport.id))  # 3
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id))  # 4
    name_flight_route = Column(String(50), nullable=False)

    fl_route1 = relationship('Airport', foreign_keys=[departure_airport_id], backref='rule_departure_airport')  # 3
    fl_route2 = relationship('Airport', foreign_keys=[arrival_airport_id], backref='rule_name_flight')  # 3 # 4

    def __str__(self):
        return self.name


# Bảng qui định chuyến bay
class Flight_regulations(BaseModel):
    __tablename__ = 'flight_regulations'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    min_onl_ticket_booking_time = Column(Integer, nullable=False)
    min_ticket_sale_time = Column(Integer, nullable=False)
    min_flight_time = Column(Integer, nullable=False)
    minimum_downtime = Column(Integer, nullable=False, default=30)
    maximum_downtime = Column(Integer, nullable=False, default=20)
    fli = relationship('Flight', backref='flight_regulations', lazy=False)  # 2

    def __str__(self):
        return self.name


# Bảng chuyen bay
class Flight(BaseModel):
    __tablename__ = 'flight'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    flight_regulations_id = Column(Integer, ForeignKey(Flight_regulations.id))  # 2
    name_flight = Column(String(50), nullable=False)
    number_empty_seats = Column(Integer, nullable=False)
    number_empty_books = Column(Integer, nullable=False)  # Thuộc tính suy diễn !
    number_seats =relationship('Number_of_seats', backref='flight', lazy=False)




#Bảng lich bay
class Flight_schedule(BaseModel):
    __tablename__ = 'flight_schedule'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    note = Column(String(50))

    def __str__(self):
        return self.name


# Bảng Hạng ghế
class Seat_class(BaseModel):
    __tablename__ = 'seat_class'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_name = Column(Integer, nullable=False)
    number_seats = relationship('Number_of_seats', backref='seat_class', lazy=False)

#Bảng số lượng ghế
class Number_of_seats(BaseModel):
    __tablename__ = 'Number_of_seats'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(Seat_class.id))
    flight_id = Column(Integer, ForeignKey(Flight.id))
    def __str__(self):
        return self.name


# Bảng Giá vé
class Fare(BaseModel):
    __tablename__ = 'fare'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    fare_value = Column(Integer, nullable=False)
    fticket = relationship('Ticket', backref='fare', lazy=False)

#Bảng Hóa đơn
class Bill(BaseModel):
    __tablename__ = 'Bill'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    fare_value = Column(Integer, nullable=False)
    date_and_time = Column(DateTime, nullable=False)
    Payment_code = Column(String(200), nullable=False)
    ticketb = relationship('Ticket', backref='Bill', lazy=False)

#Bảng nhân viên
class Staff(BaseModel):
    name = Column(String(20), nullable=False)

#Bảng nhân viên quản lý kế thừa bảng nhân viên
class management_staff(Staff):
    management_department = Column(String(30), nullable=False)


#Bảng khách hàng : Thông tin khách hàng đã được lưu chung với user


#Bảng Loại hành lý
class type_luggage(BaseModel):
    name = Column(String(20), nullable=False)
    weight_max = Column(Integer, nullable=False)

#Bảng Loaị vé
class Ticket_type(BaseModel):
    __tablename__ = 'ticket_type'
    name_Ticket_type = Column(String(60), nullable=False)
    tickett = relationship('Ticket', backref ='ticket_type', lazy=False)
#Bảng Vé
class Ticket(BaseModel):
    __tablename__ = 'ticket'
    management_department = Column(String(30), nullable=False)
    fare_id = Column(Integer, ForeignKey(Fare.id))
    bill_id = Column(Integer, ForeignKey(Bill.id))
    tick_type_id = Column(Integer, ForeignKey(Ticket_type.id))
    status = Column(String(30), nullable=False)

#########################################################
# Viết bên index nó không hiểu. Phải viết qua model nó mới hiểu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# @login.user_loader
# def load_user(user_id):
#     return dao.get_user_by_id(user_id)



if __name__ == '__main__':
    with app.app_context():


        # import hashlib
        #
        # u = User(name='admin1',
        #          passw1=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN,
        #          address='Tp.HoChiMinhcity',
        #          identification='ga',
        #          email='abcd@gmail.com',
        #          nationality='VietNam' )
        # db.session.add(u)
        # # db.session.commit()
        db.create_all()



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

