import json, os

from sqlalchemy import func

from app import app, db, flow
from flask import request
from app.model import (User,UserRoleEnum, Flight_route, Airport,
                       Flight_schedule, Flight, Flight_Flight_schedule, Flight_route_Flight, Number_of_seats, Flight_regulations,Ticket_type)
import hashlib
import re
import google.auth.transport.requests
from pip._vendor import cachecontrol
import requests
from google.oauth2 import id_token

def add_user(name, passw1, **kwargs): #biến **kwargs dùng để nhập những tham số không bắc buộc
    passw1 = str(hashlib.md5(passw1.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), passw1=passw1, email=kwargs.get('email'), avatar=kwargs.get('avatar'), address=kwargs.get('address'), identification=kwargs.get('identification'), nationality=kwargs.get('nationality'), birthdate=kwargs.get('birthdate'))
    db.session.add(user)
    db.session.commit()
    return user

def add_Airport(name):
    airport = Airport(name=name)
    db.session.add(airport)
    db.session.commit()
    return airport

def add_Flight_route(airport_from_id, airport_to_id,bw_airport_id, **kwargs):
    flight_route = Flight_route(arrival_airport_id=airport_to_id, departure_airport_id = airport_from_id,bw_airport_id=bw_airport_id, name_flight_route=kwargs.get('name_flight_route'))
    db.session.add(flight_route)
    db.session.commit()
    return flight_route


def add_Number_of_seats(seat_class_id, num, flight_id):
    number_of_seats = Number_of_seats(seat_class_id=seat_class_id, num=num, flight_id=flight_id)
    db.session.add(number_of_seats)
    db.session.commit()
    return  number_of_seats


def add_Flight_schedule(departure_time, arrival_time, **kwargs):
    flight_schedule = Flight_schedule(departure_time=departure_time, arrival_time=arrival_time, note=kwargs.get('note'))
    db.session.add(flight_schedule)
    db.session.commit()
    return flight_schedule

def add_Flight(number_empty_seats, **kwargs):
    flight = Flight(number_empty_seats=number_empty_seats,time_stop=kwargs.get('time_stop') )
    db.session.add(flight)
    db.session.commit()
    return flight

def add_Flight_Flight_schedule(flight_id, flight_schedule_id):
    flight_Flight_schedule = Flight_Flight_schedule(flight_schedule_id=flight_schedule_id, flight_id=flight_id)
    db.session.add(flight_Flight_schedule)
    db.session.commit()
    return flight_Flight_schedule

def add_Flight_route_Flight(flight_id, flight_route_id):
    flight_route_id = Flight_route_Flight(flight_route_id=flight_route_id, flight_id=flight_id)
    db.session.add(flight_route_id)
    db.session.commit()
    return flight_route_id

def kiem_tra_so(so, do_dai):
    # Định nghĩa biểu thức chính quy cho một số điện thoại cơ bản
    mau = re.compile(fr'^\d{{{do_dai}}}$')

    # Sử dụng biểu thức chính quy để so khớp với số điện thoại
    khop = mau.match(so)

    # Kiểm tra xem số điện thoại có khớp với mẫu không
    if khop:
        return True
    else:
        return False


def DuLieuSoDinhDanh():
    # Thực hiện truy vấn để lấy cột identification từ bảng User
    identifications = db.session.query(User.identification).all()

    # identifications là một danh sách các tuple, chúng ta có thể trích xuất giá trị từ mỗi tuple
    identification_values = [id[0] for id in identifications]
    return identification_values

def DuLieuEmail():
    # Thực hiện truy vấn để lấy cột email từ bảng User
    email = db.session.query(User.email).all()

    # email là một danh sách các tuple, chúng ta có thể trích xuất giá trị từ mỗi tuple

    email_values = [idE[0] for idE in email]
    return email_values


def DuLieuPass():
    pass1 = db.session.query(User.passw1).all()
    pass1_values = [id[0] for id in pass1]
    return pass1_values


def check_login(email, passw1):
    if email and passw1:
        passw1 = str(hashlib.md5(passw1.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.email.__eq__(email.strip()),
                                 User.passw1.__eq__(passw1)).first()
def check_role(role):
    if role:
        if role.__eq__('UserRoleEnum.ADMIN'):
            return 1
        else:
            return 0
def get_user_by_id(id):
    return User.query.get(id)

def get_user_oauth():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    user_oauth = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.getenv("OAUTH_CLIENT_ID")
    )
    return user_oauth


# def check_changTicket(idTicked):
#     if idTicked:
#         id_flight = Flight.query.filter_by(id=user_flight_code).first()

#lưu quy định xuống databae
def add_regulations(min_onl_ticket_booking_time, min_ticket_sale_time, min_flight_time, minimum_downtime, maximum_downtime, current_date):
    a = Flight_regulations(min_onl_ticket_booking_time=min_onl_ticket_booking_time, min_ticket_sale_time=min_ticket_sale_time, min_flight_time=min_flight_time, minimum_downtime=minimum_downtime, maximum_downtime=maximum_downtime, current_date=current_date)
    db.session.add(a)
    db.session.commit()
    return a

