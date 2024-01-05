import os.path
import pathlib
from flask_babelex import Babel
from flask import Flask
from urllib.parse import quote

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)

moment = Moment(app)

app.secret_key = '^%*&^^HJGHJGHJFD%^&%&*^*(^^^&^(*^^$%^GHJFGHJH'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/cnpm?charset=utf8mb4" % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6


db = SQLAlchemy(app=app)

login_manager = LoginManager(app=app)


client_secrets_file = os.path.join(pathlib.Path(__file__).parent.parent, "oauth_config.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://localhost:5000/callback"
)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
