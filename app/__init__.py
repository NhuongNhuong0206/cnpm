from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager

app = Flask(__name__)

app.secret_key = '^%*&^^HJGHJGHJFD%^&%&*^*(^^^&^(*^^$%^GHJFGHJH'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/cnpm?charset=utf8mb4" % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6




db = SQLAlchemy(app=app)
<<<<<<< HEAD
login = LoginManager(app=app)# khởi tạo login_manager cho app


=======
login_manager = LoginManager(app=app)
>>>>>>> d34f8fb53b4166c8f11a9380b51ef0eddeeca24a
