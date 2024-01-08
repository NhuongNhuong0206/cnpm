

from flask import render_template, request, redirect, jsonify, session, url_for
from app import app, util, controllers, dao, login_manager, admin
from validate_email import validate_email
from datetime import datetime
from flask_login import login_user, logout_user

from app.model import UserRoleEnum, Flight, Ticket_type, Ticket, Bill,User

app.add_url_rule('/api/user/confirm', 'confirm_user', controllers.confirm_user,
                 methods=['post'])

app.add_url_rule('/admin/changeTickets', 'changeTickets', dao.changeTickets,
                 methods=['post'])
app.add_url_rule('/api/admin_rules', 'create_admin_rules', dao.create_admin_rules,
                 methods=['post'])
app.add_url_rule('/api/flight-routes', 'get_flight_routes', dao.get_flight_routes,
                 methods=['get', 'post'])
app.add_url_rule('/revenue-mon-stats/<selected_value>', dao.revenue_mon_stats,
                 methods=['get'])

app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)


@app.route('/')
def index():
    # Lấy dữ liệu từ form
    ticket_type = request.form.get('ticketType')
    print(ticket_type)
    from_location = request.form.get('from')
    to_location = request.form.get('to')
    day_start = request.form.get('dayStart')
    rank_chair = request.form.get('rankChair')
    # Kiểm tra giá trị trong session

    # Kiểm tra các giá trị nhận từ form
    print(ticket_type)
    print(from_location)
    print(to_location)
    print(day_start)
    print(rank_chair)

    # Thực hiện truy vấn từ cơ sở dữ liệu
    flights_result = dao.query_flights(from_location, to_location, day_start, rank_chair)

    # Lưu kết quả vào session để sử dụng ở route /fight_list
    session['data_search'] = flights_result
    session['inp_search'] = {'from_location': from_location,
                             'to_location': to_location,
                             'day_start': day_start,
                             'ticket_type': ticket_type,
                             'rank_chair': rank_chair}
    print(session['inp_search'])

    print(session['data_search'])

    # Chuyển hướng đến trang flightList.html
    return render_template('homeAndFindFlights.html')



@app.route('/revenue-mon-stats/<selected_value>', methods=['GET'])
def revenue_mon_stats(selected_value):
    start_date = '2024-01-01 00:00:00'  # dữ liệu ngày bắt đầu trong tháng (dayf)
    end_date = '2024-01-31 00:00:00'  # Dữ liệu ngày kết thúc trong tháng (days)
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')  # định dạng lại DateTime
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')  # Định dạng lại DateTime

    ticket_types = db.session.query(Ticket_type).all()  # Lấy danh sách dữ liệu tất cả các loại vé
    ticket = db.session.query(Ticket).all()  # all vé
    bill = db.session.query(Bill).all()  # all hóa đơn
    sum = 0

    # Lấy danh sách các vé trong khoảng thời gian từ start_date đến end_date
    # Lấy dữ liệu trong bảng Ticket. Join ticket và bill. Điều kiện date_and_time trong khoảng start_day -> end_day
    ticket_date_date = (db.session.query(Ticket)
                        .join(Bill, Ticket.bill_id == Bill.id)
                        .filter(Bill.date_and_time.between(start_datetime, end_datetime))
                        .all()
                        )
    print(ticket_date_date)

    # danh sách các vé theo từng loại vé
    # print(len(ticket_types))
    for tk in ticket_date_date:  # tk chạy trong ticket_date_date đã tính ở trên
        print(ticket_date_date[tk.tick_type_id - 1].status)
        if ticket_date_date[
            tk.tick_type_id - 1].status == True:  # nếu phần tử ticket_date_date thứ tk.tick_type_id - 1 đã được bán thì cộng giá vé vào tổng
            print(tk.tick_type_id)
            sum = sum + ticket_types[tk.tick_type_id - 1].fare_value
    print(sum)

    return sum



# @app.route('/search_flights', methods=['POST'])
# def search_flights():


@app.route('/fight_list', methods=['GET', 'POST'])
def fight_list():
    # Lấy dữ liệu từ session để hiển thị trên trang flightList.html
    data_search = session.get('data_search', [])
    inp_search = session.get('inp_search', {})
    a = dao.get_airport_list()
    print(a)
    print()
    # Render trang flightList.html với dữ liệu tìm kiếm
    return render_template('flightList.html', data_search=data_search, inp_search=inp_search, a=a)


@app.route('/ticket')
def ticket():
    # Thực hiện các thao tác cần thiết và trả về template ticket.html
    return render_template('ticket.html')


# @app.route('/flight')
# def index():
#     return render_template('./admin/createFlight.html')


@app.route('/login', methods=['get', 'post'])
def login():
    er_m_num = 0
    er_m_tex = ''
    if request.method.__eq__('POST'):

        email = request.form.get('email')
        passw1 = request.form.get('passw1')
        user_1 = util.check_login(email=email, passw1=passw1)
        if user_1:
            login_user(user=user_1)
            print(user_1.user_role)
            if util.check_role(user_1.user_role).__eq__(0):
                return render_template('homeAndFindFlights.html', er_m_num=er_m_num, er_m_tex=er_m_tex)
            else:

                return redirect('/admin')
        else:
            er_m_num = 1
            er_m_tex = 'Nhập sai email hoặc mật khẩu, hãy kiểm tra'
    return render_template('signIn.html', er_m_num=er_m_num, er_m_tex=er_m_tex)


@app.route('/admin-login', methods=['post'])
def singin_admin():
    email = request.form.get('email')
    passw1 = request.form.get('passw1')
    user_1 = util.check_login(email=email, passw1=passw1, role=UserRoleEnum.ADMIN)
    if user_1:
        login_user(user=user_1)
    return redirect('/admin')


@app.route('/log-out')
def logOut():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def user_load(id):
    return util.get_user_by_id(id=id)


@app.route('/logup', methods=['get', 'post'])
def logup():
    er = 1
    er_m_num = 0
    er_m_tex = ''
    er_m = ''
    current_date = datetime.now().date()
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        birthdate = request.form.get('birthdate')
        address = request.form.get('address')
        identification = request.form.get('identification')
        nationality = request.form.get('nationality')
        phone = request.form.get('phone')
        email = request.form.get('email')
        passw1 = request.form.get('passw1')
        passw2 = request.form.get('passw2')
        if birthdate:
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()  # yyyy-mm-dd
        try:

            if not name.strip():  # kiểm tra xem tên được nhập chưa
                er_m_num = 1
                er_m_tex = 'Bạn chưa nhập Họ và tên'
            elif not birthdate or birthdate > current_date:
                er_m_num = 5
                er_m_tex = 'Bạn chưa nhập hoặc nhập Ngày sinh không hợp lệ'
            elif not identification.strip() or util.kiem_tra_so(identification, 12).__eq__(False):
                er_m_num = 7
                er_m_tex = 'Bạn chưa nhập hoặc nhập Mã định danh không hợp lệ'
            elif not phone.strip() or util.kiem_tra_so(phone, 10).__eq__(
                    False):  # kiểm tra xem số điện thoại được nhập chưa, và phải là số hay không
                er_m_num = 2
                er_m_tex = 'Bạn chưa nhập Số điện thoại hoặc số điện thoại không hợp lệ'
            elif not email.strip() or not validate_email(
                    email):  # kiểm tra xem đã nhập email chưa và đã nhập đúng định dạng email không
                er_m_num = 3
                er_m_tex = 'Bạn chưa nhập Email hoặc Email không hợp lệ'

            elif not (passw1.strip() and passw2.strip() and passw1.strip().__eq__(
                    passw2.strip())):  # kiểm tra xem mật khẩu được nhập chưa và mật khẩu có trùng nhau
                er_m_num = 4
                er_m_tex = 'Bạn chưa nhập Mật khẩu hoặc Mật khẩu không khớp'
            else:
                for dataI in util.DuLieuSoDinhDanh():
                    if dataI.__eq__(identification) == True:
                        er_m_num = 8
                        er_m_tex = 'Mã số định danh đã được đăng kí tài khoản, hãy đăng nhập'
                        print("Mã số định danh trùng")
                        break

                for dataE in util.DuLieuEmail():
                    if dataE.__eq__(email) == True:
                        er_m_num = 9
                        er_m_tex = 'Email đã được đăng kí tài khoản, hãy đăng nhập'
                        print("Email trùng")
                        break
                if not (er_m_num.__eq__(8) or er_m_num.__eq__(9)):
                    print("Không được vào")
                    if len(passw1) >= 8:
                        util.add_user(name=name, passw1=passw1, email=email, birthdate=birthdate, address=address,
                                      identification=identification, nationality=nationality, phone=phone)
                        print("vào tạo")
                        return redirect('/login')
                    else:
                        er_m_num = 6
                        er_m_tex = 'Mật khẩu phải có ít nhất 8 kí tự'
                        print('Không vào tạo')
        except Exception as ex:
            print('lỗi server')
            er_m = 'Lỗi Server'
            er = 0

    return render_template('signUp.html', er_m_num=er_m_num, er_m_tex=er_m_tex, er_m=er_m, er=er)


@app.route('/book_ticket', methods=['get', 'post'])
def book_ticket():
    if request.method == 'POST':
        # Lấy dữ liệu từ các trường input
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        id_card = request.form.get('idCard')
        nationality = request.form.get('nationality')
        expiry_date = request.form.get('expiryDate')
        card_number = request.form.get('cardNumber')
        cvv = request.form.get('cvv')


# @app.route('/api/flight-routes')



# ! Lỗi 'function' object has no attribute 'user_loader'
# @login.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

    return render_template('book_tickets.html', current_date=datetime.now().strftime('%Y-%m-%d'))



if __name__ == '__main__':
    from app.admin import *

    app.run(host='localhost', port=5000, debug=True)
