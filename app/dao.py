from app.model import Flight_regulations, User
from flask import session
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



