from flask import render_template, request, redirect,url_for, jsonify, session
from app import app, util, login_manager, controllers, flow, db
from validate_email import validate_email
from datetime import datetime
from flask_login import login_user, logout_user
from app.model import User, UserRoleEnum


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
