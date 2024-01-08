
from datetime import datetime
from sqlalchemy import func, and_
from app.model import Flight_regulations, User, Number_of_seats, Bill, Flight, Ticket, Flight_schedule,Flight_Flight_schedule \
    Flight_route, Ticket_type, Bill, Airport
from flask import session, render_template, request, jsonify
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

# Đổi vé
def changeTickets():
    input_change = request.form.get('ma_chuyen_bay')  # Lấy giá trị nhập từ người dùng

    # Thực hiện so sánh với cơ sở dữ liệu (giả sử Flight là một model)
    flight_id = Flight.query.filter_by(id=input_change).first()

    print(flight_id)
    if flight_id:
        # Nếu mã chuyến bay tồn tại trong cơ sở dữ liệu
        return 'ĐÃ VÀO ĐƯỢC'
    else:
        return render_template('error_page.html')


# def get_type_ticket():
#     t = db.session.query('Ticket_type').

def get_data_stats():
    q = db.session.query(
        Flight_route.departure_airport_id,
        Flight_route.arrival_airport_id,
        func.count(Ticket.id),
        func.sum(Ticket.ticket_price).label("total_price")
    ).join(Flight_route, Ticket.flight_route_id == Flight_route.id, isouter=True)
    q = q.group_by(Flight_route.departure_airport_id, Flight_route.arrival_airport_id).order_by(func.desc("total_price"))
    return q.all()


def month_router(val):
    start_date = '2024-01-01 00:00:00' # dữ liệu ngày bắt đầu trong tháng (dayf)
    end_date = '2024-01-31 00:00:00' # Dữ liệu ngày kết thúc trong tháng (days)
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')# định dạng lại DateTime
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')#Định dạng lại DateTime

    ticket_types = db.session.query(Ticket_type).all()  # Lấy danh sách dữ liệu tất cả các loại vé
    ticket = db.session.query(Ticket).all() # all vé
    bill = db.session.query(Bill).all() # all hóa đơn
    sum = 0
    list_sum = []
    route_list = []
    routes = db.session.query(Flight_route).all()
    airport_list = db.session.query(Airport).all()

# Lấy danh sách các vé trong khoảng thời gian từ start_date đến end_date
# Lấy dữ liệu trong bảng Ticket. Join ticket và bill. Điều kiện date_and_time trong khoảng start_day -> end_day
    ticket_date_date = (db.session.query(Ticket)
    .join(Bill, Ticket.bill_id == Bill.id)
    .join(Flight_route, Ticket.flightRouter_id == Flight_route.id)
    .filter(
        Bill.date_and_time.between(start_datetime, end_datetime)

    )
    .all()
    )
    print(ticket_date_date)
    return ticket_date_date


# Thống kê
def revenue_mon_stats(val):
    start_date = '2024-01-01 00:00:00' # dữ liệu ngày bắt đầu trong tháng (dayf)
    end_date = '2024-01-31 00:00:00' # Dữ liệu ngày kết thúc trong tháng (days)
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')# định dạng lại DateTime
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')#Định dạng lại DateTime

    ticket_types = db.session.query(Ticket_type).all()  # Lấy danh sách dữ liệu tất cả các loại vé
    ticket = db.session.query(Ticket).all() # all vé
    bill = db.session.query(Bill).all() # all hóa đơn
    sum = 0
    list_sum = []
    route_list = []
    routes = db.session.query(Flight_route).all()
    airport_list = db.session.query(Airport).all()

# # Lấy danh sách các vé trong khoảng thời gian từ start_date đến end_date
# # Lấy dữ liệu trong bảng Ticket. Join ticket và bill. Điều kiện date_and_time trong khoảng start_day -> end_day
#     ticket_date_date = (db.session.query(Ticket)
#     .join(Bill, Ticket.bill_id == Bill.id)
#     .join(Flight_route, Ticket.flightRouter_id == Flight_route.id)
#     .filter(
#         Bill.date_and_time.between(start_datetime, end_datetime)
#
#     )
#     .all()
#     )
#     print(ticket_date_date)
    ticket_date_date = month_router(1)
    print(ticket_date_date)



    for r in routes:  # trả về danh sách tuyến bay dưới dạng JSON
        deprature = airport_list[r.departure_airport_id - 1].name
        # print(deprature)
        arrival = airport_list[r.arrival_airport_id - 1].name
        # print(arrival)
        route_list += [{'id': r.id, 'name': deprature + ' - ' + arrival}]
    # print(route_list)

#danh sách các vé theo từng loại vé
    # print(len(ticket_types))
    for tk in ticket_date_date:#tk chạy trong ticket_date_date đã tính ở trên
        # print(ticket_date_date[tk.tick_type_id - 1].status)
        if ticket_date_date[tk.tick_type_id - 1].status == True:# nếu phần tử ticket_date_date thứ tk.tick_type_id - 1 đã được bán thì cộng giá vé vào tổng
            # print(tk.tick_type_id)
            sum = sum + ticket_types[tk.tick_type_id - 1].fare_value
    print(sum)



    return sum


# xuất ra tên các tuyến bay
def get_flight_routes():
    route_list = []
    routes = db.session.query(Flight_route).all()
    airport_list = db.session.query(Airport).all()

    for r in routes:# trả về danh sách tuyến bay dưới dạng JSON
        deprature = airport_list[r.departure_airport_id - 1].name

        arrival = airport_list[r.arrival_airport_id - 1].name

        route_list += [{'id': r.id, 'name': deprature + ' - ' + arrival}]
    return jsonify(route_list)

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
