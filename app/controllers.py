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

# def search_flight_schedule():
#     data = request.get_json()
#     try:
#         inp_search = dao.get_inp_search_json(af_id=data['departure_airport_id'], at_id=data['arrival_airport_id'],
#                                              time_start=data['time_start'], ticket_type=data['ticket_type'])
#
#         data_search = dao.search_flight_schedule(ap_from=data['departure_airport_id'], ap_to=data['arrival_airport_id'],
#                                                  time_start=data['time_start'], ticket_type=data['ticket_type'])
#         session['data_search'] = data_search
#         session['inp_search'] = inp_search
#     except:
#         return {
#             'status': 500,
#             'data': 'error'
#         }
#     return {
#         'status': 200,
#         'data': data_search
#     }
