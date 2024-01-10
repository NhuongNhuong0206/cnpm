//document.addEventListener('DOMContentLoaded', function () {
//    // Lắng nghe sự kiện thay đổi trạng thái của radio button
//    document.querySelectorAll('input[name="ticketType"]').forEach(function (radio) {
//        radio.addEventListener('change', function () {
//            // Nếu chọn "Vé một chiều", ẩn trường nhập ngày về
//            if (radio.id === 'ticketType-1') {
//                document.getElementById('returnDateContainer').style.display = 'none';
//            } else {
//                // Nếu chọn "Vé khứ hồi", hiện trường nhập ngày về
//                document.getElementById('returnDateContainer').style.display = 'block';
//            }
//        });
//    });
//});

//document.addEventListener('DOMContentLoaded', function () {
//    // Lắng nghe sự kiện thay đổi trạng thái của radio button
//    document.querySelectorAll('input[name="ticketType"]').forEach(function (radio) {
//        radio.addEventListener('change', function () {
//            // Nếu chọn "Vé một chiều", ẩn trường nhập ngày về
//            if (radio.id === 'ticketType-1') {
//                document.getElementById('returnDateContainer').style.display = 'none';
//            } else {
//                // Nếu chọn "Vé khứ hồi", hiện trường nhập ngày về
//                document.getElementById('returnDateContainer').style.display = 'block';
//            }
//        });
//    });
//});

// homeAndFindFlights.js
document.addEventListener("DOMContentLoaded", function () {
  var fromInput = document.getElementById("ap_from");
  var toInput = document.getElementById("ap_to");
  var airportsDataList = document.getElementById("airports");

  fromInput.addEventListener("input", function () {
    showAirportList(fromInput);
  });

  toInput.addEventListener("input", function () {
    showAirportList(toInput);
  });

  function showAirportList(input) {
    airportsDataList.innerHTML = "";

    // Fetch airport data from Flask endpoint
    fetch("/get_airports")
      .then(response => response.json())
      .then(data => {
        data.airports.forEach(function (airport) {
          var option = document.createElement("option");
          option.value = `${airport.id} - ${airport.name}`;
          airportsDataList.appendChild(option);
        });
      });
  }
});


//    document.addEventListener('DOMContentLoaded', function () {
//        document.getElementById('submit-btn').addEventListener('click', function (event) {
//            var ticketType = document.querySelector('input[name="ticketType"]:checked');
//            var fromInput = document.getElementById('ap_from');
//            var toInput = document.getElementById('ap_to');
//            var dayStartInput = document.getElementById('time_start');
//            var returnDateInput = document.getElementById('return_date');
//            var rankChairInput = document.getElementById('ticket_type');
//
//            // Kiểm tra xem tất cả các trường đã được nhập đầy đủ chưa
//            if (!ticketType || !fromInput.value || !toInput.value || !dayStartInput.value || (ticketType.value === '2' && !returnDateInput.value) || !rankChairInput.value) {
//                alert('Vui lòng nhập đầy đủ thông tin để tìm kiếm chuyến bay.');
//                event.preventDefault(); // Ngăn chặn sự kiện tìm kiếm nếu thông tin không đầy đủ
//            }
//        });
//    });


function save(){
let data = {};

    data.fromLocation = document.getElementById('ap_from').value;
    data.toLocation = document.getElementById('ap_to').value;
    data.dayStart = document.getElementById('time_start').value;
//  data.returnDate = document.getElementById('return_date').value;
    data.rankChair = document.getElementById('ticket_type').value;
    localStorage.setItem('DATA_INFO', JSON.stringify(data));
    console.log(data)
}
function list_info() {
     let dataUser = JSON.parse(localStorage.getItem('DATA_INFO'));
     console.log(dataUser)
    // Kiểm tra xem có thông tin người dùng hay không
    if (dataUser?.length !== 0) {
        document.getElementById('ap_from').value = dataUser.birthdate;
        document.getElementById('ap_to').value = dataUser.address;
        document.getElementById('time_start').value = dataUser.identification;
        document.getElementById('ticket_type').value = dataUser.phone;

    }
}

//// Trong file homeAndFindFlights.js
//function lay() {
//    let data = JSON.parse(localStorage.getItem('DATA_INFO'));
//    if (data) {
//        // Tạo một đối tượng date từ chuỗi ngày
//        let startDate = new Date(data.dayStart);
//
//        // Định dạng lại ngày theo mong muốn (ví dụ: dd/MM/yyyy)
//        let formattedStartDate = `${startDate.getDate()}/${startDate.getMonth() + 1}/${startDate.getFullYear()}`;
//
//        // Hiển thị dữ liệu vào các thẻ div
//        document.getElementById('af_to').innerText = data.fromLocation;
//        document.getElementById('ap_to').innerText = data.toLocation;
//        document.getElementById('dateInfo').innerText = ` Ngày Xuất Phát:${formattedStartDate} | Hạng Vé: ${data.rankChair}`;
////       document.getElementById('ticket_type').innerText = `Vé hạng ${data.rankChair}`;
//    }
//}

function cacheData(key, value) {
   const data = JSON.parse(localStorage.getItem('cacheData')) || {}
   data[key] = value
   localStorage.setItem('cacheData',JSON.stringify(data))
}

const selectList = document.querySelectorAll('select')
const departureDate = document.querySelector('.departure_date')

selectList.forEach(select => {
    select.onchange = (e) => {
        const value = e.target.value
        const key = e.target.name
        cacheData(key, value)
    }
})

window.onload = () => {
    const data = JSON.parse(localStorage.getItem('cacheData'))
    if (!data) return;
    selectList.forEach(select => {
        if (data[select.name]) {
            select.value = data[select.name]
        }
    })

}


// dat ve

const infoFlight = document.querySelectorAll('#info-flight > th')
const btnSubmit = document.querySelector('#btn-submit')

btnSubmit.onclick = (e) => {
    const data = {
        idFlight: infoFlight[0].innerText,
        from_to: infoFlight[1].innerText,
        airport_bw: infoFlight[2].innerText,
        time: infoFlight[3].innerText,
        chairType: infoFlight[4].innerText,
        price: infoFlight[5].innerText,
    }

    localStorage.setItem("infoTicket", JSON.stringify(data))
}

