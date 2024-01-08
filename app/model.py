from flask import session
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime

from sqlalchemy.orm import relationship, backref
from app import db, app, login_manager
from flask_login import UserMixin
import enum
from datetime import datetime
from sqlalchemy import create_engine, engine
import pandas as pd
from urllib.parse import quote
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    # active = Column(Boolean, default=True)


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


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

    ticket_id = relationship('Ticket', backref='flight_route', lazy=False)
    fl_route1 = relationship('Airport', foreign_keys=[departure_airport_id], backref='rule_departure_airport')  # 3
    fl_route2 = relationship('Airport', foreign_keys=[arrival_airport_id], backref='rule_name_flight')  # 4

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
    flight_regulations_id = Column(Integer, ForeignKey(Flight_regulations.id))  # 2
    name_flight = Column(String(50), nullable=False)
    number_empty_seats = Column(Integer, nullable=False)
    number_empty_books = Column(Integer, nullable=False)  # Thuộc tính suy diễn !


    is_active = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean,nullable=False)
    number_seats = relationship('Number_of_seats', backref='flight', lazy=False)




#Bảng lich bay
class Flight_schedule(BaseModel):
    __tablename__ = 'flight_schedule'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    note = Column(String(50))

    def __str__(self):
        return self.name




class Flight_Flight_schedule(db.Model):
    __tablename__ = 'Flight_Flight_schedule'
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_schedule_id = Column(Integer, ForeignKey(Flight_schedule.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_schedules')
    flight_schedule = relationship('Flight_schedule', backref='flight_flight_schedules')


# Bảng Hạng ghế
class Seat_class(BaseModel):
    __tablename__ = 'seat_class'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_name = Column(String(20), nullable=False)
    number_seats = relationship('Number_of_seats', backref='seat_class', lazy=False)


#Bảng số lượng ghế
class Number_of_seats(BaseModel):
    __tablename__ = 'Number_of_seats'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(Seat_class.id))
    flight_id = Column(Integer, ForeignKey(Flight.id))
    num = Column(Integer)
    def __str__(self):
        return self.name


#Bảng Hóa đơn
class Bill(BaseModel):
    __tablename__ = 'Bill'
    # id = Column(Integer, primary_key=True, autoincrement=True)
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
    fare_value = Column(Integer, nullable=False)# giá ve


#Bảng Vé
class Ticket(BaseModel):
    __tablename__ = 'ticket'
    # management_department = Column(String(30), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id))# id hóa đơn
    tick_type_id = Column(Integer, ForeignKey(Ticket_type.id))#id loại vé
    flightRouter_id = Column(Integer, ForeignKey(Flight_route.id))  # id tuyến bay
    status = Column(Boolean, nullable=False)



# Viết bên index nó không hiểu. Phải viết qua model nó mới hiểu
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#

if __name__ == '__main__':
    with app.app_context():

        db.create_all()

        # import hashlib
        # u = User(name='admin',
        #          passw1=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN,
        #          address='Tp.HoChiMinhcity',
        #          identification='ga',
        #          email='damin@gmail.com',
        #          nationality='VietNam' )
        # db.session.add(u)

        # a1 = Airport(name="Tân Sơn Nhất")
        # a2 = Airport(name="Nội Bài")
        # a3 = Airport(name="Côn Đảo")
        # a4 = Airport(name="Cà Mau")
        # a5 = Airport(name="Cần Thơ")
        # a6 = Airport(name="Phú Bài")
        # a7 = Airport(name="Vân Đồn")
        # a8 = Airport(name="Đà Nẵng")
        # a9 = Airport(name="Phú Quốc")
        # a10 = Airport(name="Vinh")
        #
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        # db.session.commit()


        # định dạng năm-tháng-ngày giờ-phút-giây
        # hoadon1 = Bill( date_and_time='2024-01-08 00:00:00', Payment_code='adadadasds')
        # hoadon2 = Bill( date_and_time='2024-01-16 00:00:00', Payment_code='adadadasds')
        # hoadon3 = Bill( date_and_time='2023-01-12 00:00:00', Payment_code='adadadasds')
        # hoadon4 = Bill( date_and_time='2024-02-01 00:00:00', Payment_code='adadadasds')
        # hoadon5 = Bill( date_and_time='2024-07-03 00:00:00', Payment_code='adadadasds')
        # hoadon6 = Bill( date_and_time='2023-02-05 00:00:00', Payment_code='adadadasds')
        # db.session.add_all([hoadon1, hoadon2, hoadon3, hoadon4, hoadon5, hoadon6])
        # db.session.commit()

        # loaive1 = Ticket_type(name_Ticket_type='Thương gia', fare_value=50000)
        # loaive2 = Ticket_type(name_Ticket_type='Thường', fare_value=20000)
        # db.session.add_all([loaive1, loaive2])
        # db.session.commit()

        # tuyenBay1 = Flight_route(departure_airport_id=1, arrival_airport_id=3, name_flight_route='TanSonNhat-ConDao')
        # tuyenBay2 = Flight_route(departure_airport_id=7, arrival_airport_id=5, name_flight_route='VanDon-CanTho')
        # db.session.add_all([tuyenBay1, tuyenBay2])
        # db.session.commit()

        # t1 = Ticket(bill_id=1, tick_type_id=1, status=True, flightRouter_id=3)
        # t2 = Ticket(bill_id=2, tick_type_id=2, status=False, flightRouter_id=2)
        # t3 = Ticket(bill_id=3, tick_type_id=1, status=True, flightRouter_id=2)
        # t4 = Ticket(bill_id=4, tick_type_id=1, status=False, flightRouter_id=4)
        # t5 = Ticket(bill_id=5, tick_type_id=2, status=True, flightRouter_id=5)
        # t7 = Ticket(bill_id=6, tick_type_id=2, status=True, flightRouter_id=4)
        # db.session.add_all([t1, t2, t3, t4, t5, t6, t7])
        # db.session.commit()


        # fl = Flight(name_flight='QuangNgai-DaNnang', number_empty_seats=30,
        #             number_empty_books=10, is_active=True, is_deleted=False)
        # db.session.add(fl)
        # db.session.commit()

        # fr = Flight_regulations(min_onl_ticket_booking_time=30, min_ticket_sale_time=20, min_flight_time=40,
        #                    minimum_downtime=50, maximum_downtime=60)
        # db.session.add(fr)
        # db.session.commit()

        # x = type_luggage(name='xach tay', weight_max=3)
        # db.session.add(x)
        # db.session.commit()
        # #
        # pass



