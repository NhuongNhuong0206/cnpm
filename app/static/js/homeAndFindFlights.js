document.addEventListener('DOMContentLoaded', function () {
    // Lắng nghe sự kiện thay đổi trạng thái của radio button
    document.querySelectorAll('input[name="ticketType"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            // Nếu chọn "Vé một chiều", ẩn trường nhập ngày về
            if (radio.id === 'ticketType-1') {
                document.getElementById('returnDateContainer').style.display = 'none';
            } else {
                // Nếu chọn "Vé khứ hồi", hiện trường nhập ngày về
                document.getElementById('returnDateContainer').style.display = 'block';
            }
        });
    });
});

