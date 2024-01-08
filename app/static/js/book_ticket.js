function DuLieuNguoiDung() {
    // Tạo đối tượng user
    let user = {};
    // Lấy giá trị từ các thẻ input và gán vào thuộc tính tương ứng của đối tượng user
    user.fullName = document.getElementById('fullName').value;
    user.email = document.getElementById('email').value;
    user.address = document.getElementById('address').value;
    user.phone = document.getElementById('phone').value;
    user.dob = document.getElementById('dob').value;
    user.idCard = document.getElementById('idCard').value;
    user.nationality = document.getElementById('nationality').value;
    user.expiryDate = document.getElementById('expiryDate').value;
    user.cardNumber = document.getElementById('cardNumber').value;
    user.cvv = document.getElementById('cvv').value;
    localStorage.setItem('USER_INFO', JSON.stringify(user));

}

function LayThongTinNguoiDung() {
     let dataUser = JSON.parse(localStorage.getItem('USER_INFO'));
    // Kiểm tra xem có thông tin người dùng hay không
    if (dataUser?.length !== 0) {
        document.getElementById('fullName').value = dataUser.fullName;
        document.getElementById('email').value = dataUser.email;
        document.getElementById('address').value =dataUser.address;
        document.getElementById('phone').value =dataUser.phone;
        document.getElementById('dob').value =dataUser.dob;
        document.getElementById('idCard').value =dataUser.idCard;
        document.getElementById('nationality').value =dataUser.nationality;
        document.getElementById('expiryDate').value =dataUser.expiryDate;
        document.getElementById('cardNumber').value =dataUser.cardNumber;
        document.getElementById('cvv').value =dataUser.cvv;
    }
}