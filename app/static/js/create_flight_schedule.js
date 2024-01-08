document.addEventListener('DOMContentLoaded', function () {
    // Lắng nghe sự kiện khi form được submit
    document.querySelector('form').addEventListener('submit', function (event) {
        // Kiểm tra giá trị các trường
        if (!validateAirports() || !validateStopTime() || !validateDateTime() || !validateTicketQuantity()) {
            // Nếu có bất kỳ lỗi nào, ngăn chặn sự kiện submit
            event.preventDefault();
        }
    });

    // Hàm kiểm tra giá trị của các trường sân bay
    function validateAirports() {
        var airportFrom = document.querySelector('select[name="airport_from"]').value;
        var airportTo = document.querySelector('select[name="airport_to"]').value;
        var airportBW = document.querySelector('select[name="airport_bw"]').value;

        // Kiểm tra xem các sân bay có giống nhau không
        if (airportFrom === airportTo || airportFrom === airportBW || airportTo === airportBW) {
            alert('Các sân bay không được trùng nhau.');
            return false;
        }
        return true;
    }

    // Hàm kiểm tra thời gian dừng
    function validateStopTime() {
        var stopTime = document.querySelector('input[name="airport_bw_stay"]').value;

        // Kiểm tra thời gian dừng không quá 60 phút
        if (parseInt(stopTime) > 60) {
            alert('Thời gian dừng không được quá 60 phút.');
            return false;
        }
        return true;
    }

     // Hàm kiểm tra thời gian đi và thời gian đến
    function validateDateTime() {
        var startTime = new Date(document.querySelector('input[name="time_start"]').value);
        var endTime = new Date(document.querySelector('input[name="time_end"]').value);

        // Kiểm tra thời gian đến và thời gian đi
        if (startTime > endTime || (endTime - startTime) < (30 * 60 * 1000) || startTime < new Date()) {
            alert('Thời gian đến phải sau thời gian đi ít nhất 30 phút và không được là ngày trong quá khứ.');
            return false;
        }
        return true;
    }

    // Hàm kiểm tra số lượng vé
    function validateTicketQuantity() {
        var quantity1st = document.querySelector('input[name="quantity_1st"]').value;
        var quantity2nd = document.querySelector('input[name="quantity_2nd"]').value;

        // Kiểm tra số lượng vé không được quá 500
        if (parseInt(quantity1st) > 500 || parseInt(quantity2nd) > 500) {
            alert('Số lượng vé không được quá 500 mỗi loại.');
            return false;
        }
        return true;
    }
});