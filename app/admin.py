from flask import redirect, session
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user

from app import app, db
from flask_admin import Admin, BaseView, expose

from app.model import User


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        session.clear()
        return redirect('/login')


admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))

