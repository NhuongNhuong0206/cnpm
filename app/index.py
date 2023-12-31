from flask import render_template, request, redirect,url_for, jsonify, session
from app import app, util
from validate_email import validate_email
from datetime import datetime

@app.route('/')
def index():
    return render_template('homeAndFindFlights.html')


@app.route('/login', methods=['get', 'post'])
def login():
    er_m_num = 0
    er_m_tex = ''
    if request.method.__eq__('POST'):

        email = request.form.get('email')
        passw1 = request.form.get('passw1')
        user_1 = util.check_login(email=email, passw1=passw1)
        print(user_1)
        if user_1:
            return render_template('homeAndFindFlights.html', er_m_num=er_m_num, er_m_tex=er_m_tex)
        else:
            er_m_num = 1
            er_m_tex = 'Lỗi'
    return render_template('signIn.html', er_m_num=er_m_num, er_m_tex=er_m_tex)


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
                    if dataI.__eq__(identification):
                        er_m_num = 8
                        er_m_tex = 'Mã số định danh đã được đăng kí tài khoản, hãy đăng nhập'
                        print("Mã số định danh trùng")
                        break

                for dataE in util.DuLieuEmail():
                    if dataE.__eq__(email):
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


if __name__ == '__main__':
    app.run(debug=True)