function DuLieuNguoiDung() {
    // Tạo đối tượng user
    let user = {};

    // Lấy giá trị từ các thẻ input và gán vào thuộc tính tương ứng của đối tượng user
    user.name = document.getElementById('name').value;
    user.birthdate = document.getElementById('birthdate').value;
    user.address = document.getElementById('address').value;
    user.identification = document.getElementById('identification').value;
    user.nationality = document.getElementById('nationality').value;
    user.phone = document.getElementById('phone').value;
    user.email = document.getElementById('email').value;
    user.passw1 = document.getElementById('passw1').value;
    user.passw2 = document.getElementById('passw2').value;
    console.log(user);
    localStorage.setItem('USER_INFO', JSON.stringify(user));
}

function LayThongTinNguoiDung() {
     let dataUser = JSON.parse(localStorage.getItem('USER_INFO'));
     console.log(dataUser)
    // Kiểm tra xem có thông tin người dùng hay không
    if (dataUser?.length !== 0) {
        document.getElementById('name').value = dataUser.name;
        document.getElementById('birthdate').value = dataUser.birthdate;
        document.getElementById('address').value = dataUser.address;
        document.getElementById('identification').value = dataUser.identification;
        document.getElementById('nationality').value = dataUser.nationality;
        document.getElementById('phone').value = dataUser.phone;
        document.getElementById('email').value = dataUser.email;
        document.getElementById('passw1').value = dataUser.passw1;
        document.getElementById('passw2').value = dataUser.passw2;
    }
}

a = document.getElementById('btn_signUp')
console.log(a)

