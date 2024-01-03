function DuLieuSign() {
    let user_Sign = {};

    // Lấy giá trị từ các thẻ input và gán vào thuộc tính tương ứng của đối tượng user
    user_Sign.email = document.getElementById('email').value;
    user_Sign.passw1 = document.getElementById('passw1').value;

    console.log(user_Sign);
    localStorage.setItem('USER_SIGN', JSON.stringify(user_Sign));
}

function LayThongTinSign() {
     let data_user_sign = JSON.parse(localStorage.getItem('USER_SIGN'));
     console.log(data_user_sign)
    // Kiểm tra xem có thông tin người dùng hay không
    if (data_user_sign?.length !== 0) {
        document.getElementById('email').value = data_user_sign.email;
         document.getElementById('passw1').value = data_user_sign.passw1;
    }
}

a = document.getElementById('btn_signUp')
console.log(a)