from app.model import Flight_regulations, User, Airport, Flight, Flight_route, \
    Flight_schedule, Flight_Flight_schedule, Number_of_seats
from flask import session, request
from app import db
import hashlib



'''
get_admin_rules_latest: lấy dữ liệu từ database. sắp xếp giảm dần và lấy giá trị đầu tiên 
'''
def get_admin_rules_latest():
    ar = Flight_regulations.query.order_by(Flight_regulations.min_ticket_sale_time.desc()).first()
    return ar


'''
get_admin_rules_list: lấy dữ liệu từ database. sắp xếp giảm dần và cho vào trong danh sách
'''
def get_admin_rules_list():
    return Flight_regulations.query.order_by(Flight_regulations.min_ticket_sale_time.desc()).all()

def create_admin_rules(min_onl_ticket_booking_time, min_ticket_sale_time, min_flight_time):
    ar = Flight_regulations(min_onl_ticket_booking_time=min_onl_ticket_booking_time,
                    min_ticket_sale_time=min_ticket_sale_time,
                    min_flight_time=min_flight_time)
    db.session.add(ar)
    db.session.commit()
    return ar

def get_user_by_id(user_id):
    session['user_cur_id'] = user_id
    return User.query.get(user_id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
def confirm_user(u_id, password):
    u = get_user_by_id(u_id)
    u = auth_user(username=u.username, password=password)
    if u:
        return True
    return False

def get_airport_list(): # hàm lấy danh sách sân bay
    return Airport.query.filter().all()


def get_flight():
    f_list = Flight.query.filter(Flight.active.__eq__(True), Flight.deleted.__eq__(False)).all()
    print(f_list)
    return f_list


def get_flight_sche():
    f_list = Flight_schedule.query.filter().all()
    return f_list


def get_airport_list(): # hàm lấy danh sách sân bay
    return Airport.query.filter().all()

def get_Airport_f(flight_route):
    return Airport.query.filter(flight_route.departure_airport_id.__eq__(Airport.id))


def get_Airport_t(flight_route):
    return Airport.query.filter(flight_route.arrival_airport_id.__eq__(Airport.id))


def get_Flight_route():
    return Flight_route.query.filter().all()
def lay_lich(list_flight):
    flight_schedules = []
    for f in list_flight:
        flight_schedules.extend(db.session.query(Flight_schedule). \
            join(Flight_Flight_schedule). \
            filter(Flight_Flight_schedule.flight_id.__eq__(f.id)).all())
    print(flight_schedules)
    return flight_schedules

def lay_chuyen_bay_ung_voi_lich_bay(list_flight_sche):
    flights_for_schedule = []
    for f in list_flight_sche:
        flights_for_schedule.extend(db.session.query(Flight_schedule).join(Flight_Flight_schedule).
                                join(Flight).filter(Flight_Flight_schedule.flight_schedule_id == f.id).all())
    # print(flights_for_schedule, 'môt')
    return flights_for_schedule


def get_Number_of_seats():
    return Number_of_seats.query.filter().all()

