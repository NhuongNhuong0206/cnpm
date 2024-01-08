from flask import render_template, request, redirect,url_for, jsonify, session
from app import dao
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from validate_email import validate_email
from app import app, util, login_manager, controllers, flow, db
from app.model import User, UserRoleEnum


def confirm_user():
    data = request.get_json()
    u = dao.confirm_user(u_id=current_user.id, password=data['password'])
    if u:
        return {
            'status': 200,
            'data': 'success'
        }
    return {
        'status': 500,
        'data': 'error'
    }

# Kiem tra xem các trường có thông tin hay không. Nếu None thì return.... còn khác None thif return ....
def create_admin_rules():
    data = request.get_json() # gán dữ liệu được lấy từ phần body của một HTML request cho data
    ar = dao.Flight_regulations(min_onl_ticket_booking_time=data['min_onl_ticket_booking_time'],
                                min_ticket_sale_time=data['min_ticket_sale_time'],
                                min_flight_time=data['min_flight_time'])
    if ar is None:
        return {
            'status': 500,
            'data': 'error'
        }
    return {
        'status': 200,
        'data': 'success'
    }

def login_oauth():
    authorization_url, state = flow.authorization_url()#authorization_url đường link đến trang đăng nhập bằng gg
    print(authorization_url)
    return redirect(authorization_url) #sau khi đăng nhập xong trả về đường này authorization_url


def oauth_callback():
    try:
        user_oauth = util.get_user_oauth()
        print(user_oauth)
        email = user_oauth['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            import hashlib
            password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
            fullname = user_oauth['name']
            image = user_oauth['picture']
            user = util.add_user(name=fullname, email=email, passw1=password, avatar=image)
        login_user(user=user)
        if user.user_role == UserRoleEnum.ADMIN:
            return redirect('/admin')
    except Exception as err:
        print("err", err)
        return render_template('homeAndFindFlights.html')
    return render_template('homeAndFindFlights.html')
