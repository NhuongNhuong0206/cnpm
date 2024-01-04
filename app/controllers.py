from flask import request

from app import dao
from flask_login import current_user





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
