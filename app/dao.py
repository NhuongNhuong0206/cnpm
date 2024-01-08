from datetime import datetime

from sqlalchemy import func, and_

from app.model import Flight_regulations, User, Number_of_seats, Bill, Flight, Ticket, Flight_schedule, \
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










