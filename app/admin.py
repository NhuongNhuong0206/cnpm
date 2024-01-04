from flask import redirect, session
from flask_admin.contrib.sqla import ModelView
from app import app, db, dao, login_manager
from flask_admin import Admin, BaseView, expose, AdminIndexView

from app.model import Airport, Flight_route, UserRoleEnum, User
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


admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4',index_view=MyAdminView())
admin.add_view(AirportView(Airport, db.session, name="SÂN BAY"))
admin.add_view(Flight_routerView(Flight_route, db.session, name="TUYẾN BAY"))
admin.add_view(AdminStartView(name='Báo cáo thống kê'))
admin.add_view(RulesView(name='Thay đổi chuyến bay'))
admin.add_view(LogoutView(name='Đăng xuất'))