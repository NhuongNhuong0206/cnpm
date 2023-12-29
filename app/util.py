import json, os
from app import app, db
from app.model import User
import hashlib
import re


def add_user(name, passw1, **kwargs): #biến **kwargs dùng để nhập những tham số không bắc buộc
    passw1 = str(hashlib.md5(passw1.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), passw1=passw1, email=kwargs.get('email'), avatar=kwargs.get('avatar'), address=kwargs.get('address'), identification=kwargs.get('identification'), nationality=kwargs.get('nationality'), birthdate=kwargs.get('birthdate'))
    db.session.add(user)
    db.session.commit()


def kiem_tra_so(so, do_dai):
    # Định nghĩa biểu thức chính quy cho một số điện thoại cơ bản
    mau = re.compile(fr'^\d{{{do_dai}}}$')

    # Sử dụng biểu thức chính quy để so khớp với số điện thoại
    khop = mau.match(so)

    # Kiểm tra xem số điện thoại có khớp với mẫu không
    if khop:
        return True
    else:
        return False


def DuLieuSoDinhDanh():
    # Thực hiện truy vấn để lấy cột identification từ bảng User
    identifications = db.session.query(User.identification).all()

    # identifications là một danh sách các tuple, chúng ta có thể trích xuất giá trị từ mỗi tuple
    identification_values = [id[0] for id in identifications]
    return identification_values

