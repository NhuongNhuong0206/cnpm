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


def query_flights(from_location, to_location, day_start, rank_chair):
    # Thực hiện xử lý truy vấn ở đây
    # Chú ý: Bạn cần điều chỉnh query dựa trên cấu trúc thực tế của cơ sở dữ liệu của bạn

    flights_result = db.session.query(
        Flight,
        Flight_route,
        Airport.name.label('departure_airport_name'),
        # Thêm các trường cần thiết khác tại đây
    ).join(
        Flight_route, Flight.id == Flight_route.id
    ).join(
        Airport, Flight_route.departure_airport_id == Airport.id
    ).filter(
        Airport.id == from_location,
        Airport.id == to_location,
        # Thêm các điều kiện tìm kiếm khác tại đây
    ).all()

    # Trả về danh sách kết quả
    return flights_result
# def get_Flight_route():
#     return Flight_route.query.filter().all()
# def query_flights(search_data):
#     # Thực hiện truy vấn để lấy thông tin chuyến bay phù hợp dựa trên dữ liệu tìm kiếm
#     flights = (
#         db.session.query(
#             Flight,
#             Flight_route,
#             Flight_schedule,
#             Airport,
#             Number_of_seats,
#             Ticket_type,
#             Fare
#         )
#         .join(Flight_route_Flight, Flight.id == Flight_route_Flight.flight_id)
#         .join(Flight_route, Flight_route_Flight.flight_route_id == Flight_route.id)
#         .join(Flight_schedule, Flight.id == Flight_Flight_schedule.flight_id)
#         .join(Airport, Flight_route.departure_airport_id == Airport.id)
#         .join(Number_of_seats, Flight.id == Number_of_seats.flight_id)
#         .join(Ticket_type, Ticket_type.id == Number_of_seats.seat_class_id)
#         .join(Fare, Fare.id == Number_of_seats.flight_id_id)
#         .filter(
#             # Áp dụng các điều kiện lọc từ dữ liệu tìm kiếm
#             Flight_route.departure_airport_id == search_data['departure_airport']['id'],
#             Flight_route.arrival_airport_id == search_data['arrival_airport']['id'],
#             # Thêm điều kiện khác tùy thuộc vào yêu cầu của bạn
#         )
#         .all()
#     )

    # Xử lý kết quả và trả về danh sách chuyến bay
    # result_flights = []
    # for flight, flight_route, flight_schedule, airport, num_seats, ticket_type, fare in flights:
    #     # Xử lý dữ liệu và thêm vào result_flights
    #     result_flights.append({
    #         'time_start': flight_schedule.departure_time,
    #         'time_end': flight_schedule.arrival_time,
    #         'fl_route1': airport,  # Sân bay xuất phát
    #         'fl_router2': flight_route.fl_route2,  # Sân bay đến
    #         'airport_between_list': [],  # Cần xử lý
    #         'price': fare.fare_value,
    #         'quantity_ticket_1st': num_seats.num,  # Số lượng ghế hạng thương gia
    #         'quantity_ticket_2nd': num_seats.num,  # Số lượng ghế hạng phổ thông
    #         'quantity_ticket_1st_booked': 0,  # Cần xử lý
    #         'quantity_ticket_2nd_booked': 0,  # Cần xử lý
    #     })
    #
    # return result_flights
