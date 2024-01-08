
from flask import render_template, request, redirect, jsonify, session, url_for
from sqlalchemy.sql.functions import rollup

from app import app, util, controllers, dao, login_manager, admin
from validate_email import validate_email
from datetime import datetime
from flask_login import login_user, logout_user
from app.model import UserRoleEnum


from app.model import User, UserRoleEnum

app.add_url_rule('/api/admin_rules', 'create_admin_rules', dao.create_admin_rules,
                 methods=['post'])
app.add_url_rule('/api/user/confirm', 'confirm_user', controllers.confirm_user,
                 methods=['post'])


app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)


@app.route('/')
def index():
    return render_template('homeAndFindFlights.html')


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

            if not name.strip(): #kiểm tra xem tên được nhập chưa
                er_m_num = 1
                er_m_tex = 'Bạn chưa nhập Họ và tên'
            elif not birthdate or birthdate > current_date:
                er_m_num = 5
                er_m_tex = 'Bạn chưa nhập hoặc nhập Ngày sinh không hợp lệ'
            elif not identification.strip() or util.kiem_tra_so(identification, 12).__eq__(False):
                er_m_num = 7
                er_m_tex = 'Bạn chưa nhập hoặc nhập Mã định danh không hợp lệ'
            elif not phone.strip() or util.kiem_tra_so(phone, 10).__eq__(False): # kiểm tra xem số điện thoại được nhập chưa, và phải là số hay không
                er_m_num = 2
                er_m_tex = 'Bạn chưa nhập Số điện thoại hoặc số điện thoại không hợp lệ'
            elif not email.strip() or not validate_email(email):#kiểm tra xem đã nhập email chưa và đã nhập đúng định dạng email không
                er_m_num = 3
                er_m_tex = 'Bạn chưa nhập Email hoặc Email không hợp lệ'

            elif not (passw1.strip() and passw2.strip() and passw1.strip().__eq__(passw2.strip())):# kiểm tra xem mật khẩu được nhập chưa và mật khẩu có trùng nhau
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

    return render_template('book_tickets.html', current_date=datetime.now().strftime('%Y-%m-%d'))
@app.route('/pay', methods=['get', 'post'])
def pay():
    return render_template('pay.html')

# ! Lỗi 'function' object has no attribute 'user_loader'
# @login.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


if __name__ == '__main__':
    from app.admin import *

    app.run(host='localhost', port=5000, debug=True)

