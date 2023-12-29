from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)

class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    passw1 = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    address = Column(String(100))
    identification = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    nationality = Column(String(50), nullable=False)
    birthdate = Column(DateTime)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
