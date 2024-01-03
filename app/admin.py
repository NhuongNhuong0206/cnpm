from flask_admin.contrib.sqla import ModelView
from app import app, db, dao
from flask_admin import Admin, BaseView, expose
from app.model import  Airport, Flight_route, UserRoleEnum
from flask_login import current_user






admin = Admin(app=app, name='QUẢN TRỊ ADMIN', template_mode='bootstrap4')

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
#
#
class AuthenticatedUser(BaseView):
    def is_accessible(self):

        return current_user.is_authenticated




# giao dien san bay
class AirportView(ModelView):
    # colum_list = ('id', 'name') Hien thi cac cot ra man hinh
    colum_list = ['id', 'name']
    can_export = True
    edit_modal = True

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


#Giao dien tuyen bay
class Flight_routerView(ModelView):
    column_list = [' id', 'departure_airport_id',  ' name_flight_route']




# Thay doi chuyến bay
class RulesView(BaseView):
    @expose('/')
    def index(self):
        rules = dao.get_admin_rules_latest()
        rules_list = dao.get_admin_rules_list()
        return self.render('admin/rules.html', rules=rules, rules_list=rules_list)

# Báo cáo thống kê
class AdminStartView(BaseView):
    @expose("/")
    def router(self):
        return self.render('admin/stats.html')

admin.add_view(AirportView(Airport, db.session, name="SÂN BAY"))
admin.add_view(Flight_routerView(Flight_route, db.session, name="TUYẾN BAY"))
admin.add_view(AdminStartView(name='Báo cáo thống kê'))
admin.add_view(RulesView(name='Thay đổi chuyến bay'))




