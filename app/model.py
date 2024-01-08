from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime,Date, PrimaryKeyConstraint
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
    STAFF = 3


# Bảng sân bay
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
    bw_airport_id = Column(Integer, ForeignKey(Airport.id))
    name_flight_route = Column(String(50), nullable=False)

    fl_route1 = relationship('Airport', foreign_keys=[departure_airport_id], backref='rule_departure_airport')  # 3
    fl_route2 = relationship('Airport', foreign_keys=[arrival_airport_id], backref='rule_name_flight')  # 3 # 4
    fl_route3 = relationship('Airport', foreign_keys=[bw_airport_id], backref='rule_name_flight_3')


    def __str__(self):
        return self.name_flight_route


class Flight_Flight_schedule(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_schedule_id = Column(Integer, ForeignKey(Flight_schedule.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_schedules')
    flight_schedule = relationship('Flight_schedule', backref='flight_flight_schedules')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_schedule_id'),
        )

class Flight_route_Flight(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_route_id = Column(Integer, ForeignKey(Flight_route.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_route')
    flight_route = relationship('Flight_route', backref='flight_flight_route')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_route_id'),
        )


# Bảng Hạng ghế
class Seat_class(BaseModel):
    __tablename__ = 'seat_class'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_name = Column(String(20), nullable=False)
    number_seats = relationship('Number_of_seats', backref='seat_class', lazy=False)


# Bảng số lượng ghế
class Number_of_seats(BaseModel):
    __tablename__ = 'Number_of_seats'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(Seat_class.id))
    flight_id = Column(Integer, ForeignKey(Flight.id))
    num = Column(Integer)

    def __str__(self):
        return self.name





# Bảng Hóa đơn
class Bill(BaseModel):
    __tablename__ = 'Bill'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    fare_value = Column(Integer, nullable=False)
    date_and_time = Column(DateTime, nullable=False)
    Payment_code = Column(String(200), nullable=False)
    ticketb = relationship('Ticket', backref='Bill', lazy=False)


# Bảng nhân viên
class Staff(BaseModel):
    name = Column(String(20), nullable=False)


# Bảng nhân viên quản lý kế thừa bảng nhân viên
class management_staff(Staff):
    management_department = Column(String(30), nullable=False)


# Bảng khách hàng : Thông tin khách hàng đã được lưu chung với user


# Bảng Loại hành lý
class type_luggage(BaseModel):
    name = Column(String(20), nullable=False)
    weight_max = Column(Integer, nullable=False)


# Bảng Loaị vé
class Ticket_type(BaseModel):
    __tablename__ = 'ticket_type'

    name_Ticket_type = Column(String(60), nullable=False)
    fare_value = Column(Integer, nullable=False)
    tickett = relationship('Ticket', backref='ticket_type', lazy=False)
    
    
# Bảng Khách hàng
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
    birthdate = Column(Date)
    # phone_number = Column(Integer)

    def __str__(self):
        return self.name


#Bảng sân bay
class Airport(BaseModel):
    __tablename__ = 'airport'
    name = Column(String(50), nullable=True)


    def __str__(self):
        return self.name


# Bảng qui định chuyến bay
class Flight_regulations(BaseModel):
    __tablename__ = 'flight_regulations'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    min_onl_ticket_booking_time = Column(Integer, nullable=False)#thời gian mua vé onl tối thiểu
    min_ticket_sale_time = Column(Integer, nullable=False)#thời gian bán vé tối thiểu
    min_flight_time = Column(Integer, nullable=False)#thời gian bay tối thiểu
    minimum_downtime = Column(Integer, nullable=False, default=30)#thời gian dừng tối thiểu
    maximum_downtime = Column(Integer, nullable=False, default=20)#thời gian dừng tối da
    current_date = Column(Date)
    def __str__(self):
        return self.min_onl_ticket_booking_time


# Bảng chuyen bay
class Flight(BaseModel):
    __tablename__ = 'flight'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name_flight = Column(String(50))
    number_empty_seats = Column(Integer, nullable=False)
    number_empty_books = Column(Integer)  # Thuộc tính suy diễn !
    time_stop = Column(Integer)

    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    number_seats = relationship('Number_of_seats', backref='flight', lazy=False)

    # number_flight = relationship('Flight_Flight_schedule', backref='flight', lazy=False)
    def __str__(self):
        return self.time_stop


#Bảng lich bay
class Flight_schedule(BaseModel):
    __tablename__ = 'flight_schedule'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime) #, nullable=False
    arrival_time = Column(DateTime) #, nullable=False
    note = Column(String(50))

    # number_schedule = relationship('Flight_Flight_schedule', backref='flight_schedule', lazy=False)

    def __str__(self):
        return self.note


class Flight_Flight_schedule(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_schedule_id = Column(Integer, ForeignKey(Flight_schedule.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_schedules')
    flight_schedule = relationship('Flight_schedule', backref='flight_flight_schedules')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_schedule_id'),
    )

    def __str__(self):
        return self.flight_id


class Flight_route_Flight(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_route_id = Column(Integer, ForeignKey(Flight_route.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_route')
    flight_route = relationship('Flight_route', backref='flight_flight_route')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_route_id'),
    )



# Bảng Hạng ghế
class Seat_class(BaseModel):
    __tablename__ = 'seat_class'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_name = Column(String(20), nullable=False)
    number_seats = relationship('Number_of_seats', backref='seat_class', lazy=False)

    def __str__(self):
        return self.seat_class_name

#Bảng số lượng ghế
class Number_of_seats(BaseModel):
    __tablename__ = 'Number_of_seats'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(Seat_class.id))
    flight_id = Column(Integer, ForeignKey(Flight.id))
    num = Column(Integer)
    def __str__(self):
        return self.Number_of_seats


# Bảng Giá vé
class Fare(BaseModel):
    __tablename__ = 'fare'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    fare_value = Column(Integer, nullable=False)
    fticket = relationship('Ticket', backref='fare', lazy=False)

    def __str__(self):
        return self.Fare

#Bảng Hóa đơn
class Bill(BaseModel):
    __tablename__ = 'Bill'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    fare_value = Column(Integer, nullable=False)
    date_and_time = Column(DateTime, nullable=False)
    Payment_code = Column(String(200), nullable=False)
    ticketb = relationship('Ticket', backref='Bill', lazy=False)

    def __str__(self):
        return self.Bill

#Bảng nhân viên
class Staff(BaseModel):
    name = Column(String(20), nullable=False)

# Bảng Vé
class Ticket(BaseModel):
    __tablename__ = 'ticket'
    #management_department = Column(String(30), nullable=False)

    bill_id = Column(Integer, ForeignKey(Bill.id))
    tick_type_id = Column(Integer, ForeignKey(Ticket_type.id))

    status = Column(Boolean, nullable=False)
    def __str__(self):
        return self.Tiket
      
      
#Bảng nhân viên quản lý kế thừa bảng nhân viên
class management_staff(Staff):
    management_department = Column(String(30), nullable=False)

    def __str__(self):
        return self.management_staff
#Bảng khách hàng : Thông tin khách hàng đã được lưu chung với user


#Bảng Loại hành lý
class type_luggage(BaseModel):
    name = Column(String(20), nullable=False)
    weight_max = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


#Bảng Loaị vé
class Ticket_type(BaseModel):
    __tablename__ = 'ticket_type'
    name_Ticket_type = Column(String(60), nullable=False)
    tickett = relationship('Ticket', backref ='ticket_type', lazy=False)

    def __str__(self):
        return self.Ticket_type
#Bảng Vé
class Ticket(BaseModel):
    __tablename__ = 'ticket'
    management_department = Column(String(30), nullable=False)
    fare_id = Column(Integer, ForeignKey(Fare.id))
    bill_id = Column(Integer, ForeignKey(Bill.id))
    tick_type_id = Column(Integer, ForeignKey(Ticket_type.id))
    status = Column(String(30), nullable=False)

    def __str__(self):
        return self.Ticket
      
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
        # u = User(name='admin1',
        #          passw1=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN,
        #          address='Tp.HoChiMinhcity',
        #          identification='ga',
        #          email='abcd@gmail.com',
        #          nationality='VietNam' )
        # db.session.add(u)
        # db.session.commit()
        # db.create_all()

        #
        # a1 = Airport(name='Tân Sơn Nhất')
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
        # q1 = Flight_regulations(min_onl_ticket_booking_time = 50 ,  min_ticket_sale_time = 70,  min_flight_time = 60 )
        #
        #
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        # db.session.add_all([a1, a2])
        # db.session.add(q1)
        # db.session.commit()
        
# # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
    # # Tuyến bay
    #     x1=Flight_route(departure_airport_id=1,arrival_airport_id=2,bw_airport_id=3,name_flight_route="Tân Sơn nhất - Hà nội")
    #     x2=Flight_route(departure_airport_id=1,arrival_airport_id=3,bw_airport_id=4,name_flight_route="Tân Sơn nhất - Côn Đảo")
    #     x3=Flight_route(departure_airport_id=1,arrival_airport_id=4,bw_airport_id=5,name_flight_route="Tân Sơn nhất - Cà Mau ")
    #     db.session.add_all([x1,x2,x3])
    #     db.session.commit()
    #
        # b1=Flight(name_flight="chuyến 1",number_empty_seats=20,number_empty_books=15,active=1,deleted=0)
        # b2=Flight(name_flight="chuyến 2",number_empty_seats=15,number_empty_books=25,active=1,deleted=0)
        # b3=Flight(name_flight="chuyến 3",number_empty_seats=19,number_empty_books=16,active=1,deleted=0)
        # db.session.add_all([b1, b2, b3])
        # db.session.commit()
    #
        # d1 = Flight_schedule(departure_time="2024-01-20 16:30:00", arrival_time="2024-01-20 18:30:00")
        # d2 = Flight_schedule(departure_time="2024-01-21 16:30:00", arrival_time="2024-01-21 18:30:00")
        # d3 = Flight_schedule(departure_time="2024-01-22 16:30:00", arrival_time="2024-01-22 18:30:00")
        # db.session.add_all([d1, d2, d3])
        # db.session.commit()
    #
        # c1 = Flight_route_Flight(flight_id=1,flight_route_id=2)
        # c2 = Flight_route_Flight(flight_id=2, flight_route_id=3)
        # c3 = Flight_route_Flight(flight_id=3, flight_route_id=4)
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
    #
    #
    #
        # e1=Flight_Flight_schedule(flight_id=1,flight_schedule_id=1)
        # e2=Flight_Flight_schedule(flight_id=1,flight_schedule_id=2)
        # e3=Flight_Flight_schedule(flight_id=2, flight_schedule_id=2)
        # db.session.add_all([e1, e2, e3])
        # db.session.commit()
    # #
    #     loaive1 = Ticket_type(name_Ticket_type='Thương gia', fare_value=50000)
    #     loaive2 = Ticket_type(name_Ticket_type='Thường', fare_value=20000)
    #     db.session.add_all([loaive1, loaive2])
    #     db.session.commit()
    #
        # t1 = Ticket(tick_type_id=1, status=True)
        # t2 = Ticket(tick_type_id=2, status=False)
        # t3 = Ticket(tick_type_id=1, status=True)
        # t4 = Ticket(tick_type_id=1, status=False)
        # t5 = Ticket(tick_type_id=2, status=True)
        # t6 = Ticket(tick_type_id=1, status=True)
        # t7 = Ticket(tick_type_id=2, status=True)
        # db.session.add_all([t1, t2, t3, t4, t5, t6, t7])
        # db.session.commit()
        
        # g1= Seat_class(seat_class_name='Hạng thương gia')
        # g2 = Seat_class(seat_class_name='Hạng thường')
        # db.session.add_all([g1, g2])
        # db.session.commit()
        pass
