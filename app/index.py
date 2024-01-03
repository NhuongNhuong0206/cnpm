from flask import render_template, request, redirect, jsonify, session
from app import app, util, controllers
from validate_email import validate_email
from datetime import datetime

from app.model import User
app.add_url_rule('/api/admin_rules', 'create_admin_rules', controllers.create_admin_rules,
                 methods=['post'])
app.add_url_rule('/api/user/confirm', 'confirm_user', controllers.confirm_user,
                 methods=['post'])


@app.route('/')
def index():
    return render_template('homeAndFindFlights.html')


@app.route('/login')
def login():
    return render_template('signIn.html')


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
                for data in util.DuLieuSoDinhDanh():

                    if data.__eq__(identification):
                        er_m_num = 8
                        er_m_tex = 'Mã số định danh đã được đăng kí tài khoản, hãy đăng nhập'
                        break
                if not er_m_num.__eq__(8):
                    if len(passw1) >= 8:
                        util.add_user(name=name, passw1=passw1, email=email, birthdate=birthdate, address=address,
                                      identification=identification, nationality=nationality, phone=phone)
                        return redirect('/login')
                    else:
                        er_m_num = 6
                        er_m_tex = 'Mật khẩu phải có ít nhất 8 kí tự'
                        print('lỗi nè')

        except Exception as ex:
            er_m = 'Có lỗi ' + str(ex)
            er = 0

    return render_template('signUp.html', er_m_num=er_m_num, er_m_tex=er_m_tex, er_m=er_m, er=er)




# ! Lỗi 'function' object has no attribute 'user_loader'
# @login.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))




if __name__ == '__main__':
    from app import admin


    app.run(debug=True)