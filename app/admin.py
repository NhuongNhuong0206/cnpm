from flask import redirect, session, request, render_template, url_for
from flask_admin.contrib.sqla import ModelView
from app import app, db, dao, login_manager, util
from flask_admin import Admin, BaseView, expose, AdminIndexView
from datetime import datetime

from app.model import Airport, Flight_route, UserRoleEnum, User, Flight
from flask_login import current_user, logout_user



'''Gán điều kiện khi đăng nhập admin thì mới có quyền thấy các cái option kế thừa từ nó'''
class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
#
#
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# giao dien san bay
class AirportView(AuthenticatedAdmin):
    # colum_list = ('id', 'name') Hien thi cac cot ra man hinh
    colum_list = ['id', 'name']
    can_export = True
    edit_modal = True
    can_view_details = True


class AuthenticatedAdmin(AuthenticatedAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

      
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/login')
        if current_user.user_role == UserRoleEnum.USER:
            return redirect('/')
        return self.render('admin/index.html')


'''Đăng xuất admin'''
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        session.clear()
        return redirect('/admin')

    def ís_accessible(self):
         return current_user.is_authenticated


#Giao dien tuyen bay
class Flight_routerView(AuthenticatedAdmin):
    column_list = [' id', 'departure_airport_id',  ' name_flight_route']
    can_view_details = True


    
# quy định bay
# class RulesView(BaseView):
#     @expose('/')
#     def index(self):
#         rules = dao.get_admin_rules_latest()
#         rules_list = dao.get_admin_rules_list()
#         return self.render('admin/rules.html', rules=rules, rules_list=rules_list)

      
# Báo cáo thống kê
class AdminStartView(BaseView):
    @expose("/")
    def router(self):
        return self.render('admin/stats.html')



class AuthenticatedStaff(ModelView): # kiểm tra xem có phải nhân viên không
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN # SỬA LẠI THÀNH STAFF


class regulationsView(BaseView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        a = []
        if request.method == 'POST':
            booking_time = request.form.get('bookingTime')
            selling_time = request.form.get('sellingTime')
            flight_time = request.form.get('flightTime')
            min_stop_time = request.form.get('minStopTime')
            max_stop_time = request.form.get('maxStopTime')
            current_date = datetime.now().strftime('%Y-%m-%d')
            a = util.add_regulations(min_onl_ticket_booking_time=booking_time, min_ticket_sale_time=selling_time, min_flight_time=flight_time, minimum_downtime=min_stop_time,maximum_downtime=max_stop_time, current_date=current_date)
        return self.render('admin/regulations.html', a=a)


class FlightScheView(AuthenticatedStaff):
    print('Băt đầu vào')

    @expose('/', methods=['POST', 'GET'])
    def index(self):
        airport_list = []
        flight_list = []
        list_flight_sche = []
        a = []
        airport_list = dao.get_airport_list()  # gọi hàm lấy danh sách sân bay lưu vào biến
        if request.method == 'POST':
            print('Vào được trong index')
            airport_from = request.form.get('airport_from')
            airport_to = request.form.get('airport_to')
            time_start = request.form.get('time_start')
            time_end = request.form.get('time_end')

            quantity_1st = request.form.get('quantity_1st')
            quantity_2nd = request.form.get('quantity_2nd')
            airport_bw = request.form.get('airport_bw')
            airport_bw_stay = request.form.get('airport_bw_stay')
            airport_bw_note = request.form.get('airport_bw_note')
            if time_start and time_end:
                time_start = datetime.strptime(time_start, "%Y-%m-%dT%H:%M")
                time_end = datetime.strptime(time_end, "%Y-%m-%dT%H:%M")
            ap = util.add_Flight_route(airport_from_id=airport_from, airport_to_id=airport_to, bw_airport_id=airport_bw)
            time = util.add_Flight_schedule(departure_time=time_start, arrival_time=time_end,
                                            note=airport_bw_note)
            if quantity_1st and quantity_2nd:
                num_chair = int(quantity_1st) + int(quantity_2nd)
                flight = util.add_Flight(number_empty_seats=num_chair, time_stop=airport_bw_stay)
                num_1st = util.add_Number_of_seats(seat_class_id=1, num=int(quantity_1st), flight_id=flight.id)
                num_2nd = util.add_Number_of_seats(seat_class_id=2, num=int(quantity_2nd), flight_id=flight.id)
                flight_Flight_schedule = util.add_Flight_Flight_schedule(flight_schedule_id=time.id, flight_id=flight.id)

        flight_list = dao.get_flight()# lấy tất cả các chuyến bay

        list_light_route = dao.get_Flight_route()# lấy tất cả tuyến bay

        # list_flight_sche = dao.get_flight_sche()# lấy tất cả các lịch bay
        list_flight_sche = dao.lay_lich(flight_list)
        a = dao.lay_chuyen_bay_ung_voi_lich_bay(list_flight_sche)#trả ra chuyến bay
        list_num = dao.get_Number_of_seats()
        # print(list_light_route[1].arrival_airport_id)
        return self.render('admin/create_flight_schedule.html',
                           airport_list=airport_list, list_flight_sche=list_flight_sche,
                           a=a, list_light_route=list_light_route, flight_list=flight_list, list_num=list_num)



@app.route('/delete_flight/<int:flight_id>', methods=['POST'], endpoint='delete_flight')
def delete_flight(flight_id):

    list = dao.get_flight()
    for l in list:
        if l.id.__eq__(flight_id):
            l.deleted = True
            db.session.commit()
    return_url = request.form.get('return_url', '/admin/flight')
    # Sau khi xoá, redirect về trang hiển thị danh sách chuyến bay
    return redirect(return_url)



# class CheckFlightScheView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/check_filght.html', rules=rules, rules_list=rules_list)



admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4',index_view=MyAdminView())
admin.add_view(AirportView(Airport, db.session, name="SÂN BAY"))
admin.add_view(Flight_routerView(Flight_route, db.session, name="TUYẾN BAY"))
admin.add_view(AdminStartView(name='Báo cáo thống kê'))
# admin.add_view(RulesView(name='Lập quy đinh'))
admin.add_view(FlightScheView(Flight, db.session, name='Lịch chuyến bay'))
admin.add_view(regulationsView(name='Lập quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))