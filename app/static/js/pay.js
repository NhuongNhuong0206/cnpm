const prices = document.querySelectorAll('.price')
const infoCustomer = document.querySelectorAll('#info-customer > div > input')
const infoTicket = document.querySelectorAll('#info-ticket > div > input')
const btnMomoPay = document.querySelector("#btn-momo-payment")
const btnTienmat = document.querySelector("#btn-tienmat")

const data = JSON.parse(localStorage.getItem("infoTicket"))

window.onload = () => {
    prices.forEach(p => p.innerHTML = data.price)

    infoCustomer[0].value = data.customer.fullName
    infoCustomer[1].value = data.customer.phone
    infoCustomer[2].value = data.customer.email

    infoTicket[0].value = data.from_to
    infoTicket[1].value = data.time
    infoTicket[2].value = data.airport_bw
    infoTicket[3].value = data.chairType
}

btnMomoPay.onclick = () => {
    const price = data.price.split(" ")[0]

    const dataObj = {
        infoCustomer: data.customer,
        flightId: data.idFlight,
        total: price,
    }

    fetch(`/api/momo_payment`, {
        method: 'post',
        body: JSON.stringify(dataObj),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(res => res.json())
        .then(data => {

            if (data.resultCode === 0) {
                window.location.href = data.payUrl
            }
        })

}
//btnTienmat.onclick = () => {
//    const price = data.price.split(" ")[0]
//
//    const dataObj = {
//        infoCustomer: data.customer,
//        flightId: data.idFlight,
//        total: price,
//    }
//
//    fetch(`/api/ticket`, {
//        method: 'post',
//        body: JSON.stringify(dataObj),
//        headers: {
//            "Content-Type": "application/json"
//        }
//    })
//        .then(res => res.json())
//        .then(data => {
//
//            if (data.resultCode === 0) {
//                window.location.href = data.payUrl
//            }
//        })
//
//}
