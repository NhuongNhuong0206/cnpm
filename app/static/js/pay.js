const btnMomoPay = document.querySelector("#btn-momo-payment")
console.log(btnMomoPay)

btnMomoPay.onclick = () => {
    const data = {
        total: "700000",
        userId: 1,
    }

    fetch(`/api/momo_payment`, {
        method: 'post',
        body: JSON.stringify(data),
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
