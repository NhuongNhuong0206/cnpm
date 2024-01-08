
    const submitBtn = document.querySelector('#submit-btn')

    const authUser = (status, data) => {
        const title = status == 'error' ? 'Mật khẩu không chính xác! Vui lòng thử lại!' : 'Xác nhận mật khẩu'
        return Swal.fire({
          title,
          input: 'password',
          inputAttributes: {
            autocapitalize: 'off'
          },
          showCancelButton: true,
          confirmButtonText: 'Xác nhận',
          cancelButtonText: 'Huỷ',
          showLoaderOnConfirm: true,
          preConfirm: (password) => {
            return fetch(`/api/user/confirm`, {
                method: 'post',
                body: JSON.stringify({
                    password: password.trim()
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
              .then(response => response.json())
          },
          allowOutsideClick: () => !Swal.isLoading()
          }).then((result) => {
            if (result.isConfirmed) {
                if (result?.value.status == 200) {
                    fetch("/api/admin_rules", {
                        method: 'post',
                        body: JSON.stringify(data),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        window.location.reload()
                    })
                    .catch(err => {
                        return Swal.fire("Lỗi", err.response, "error");
                    })
                }
                if (result?.value.status == 500) {
                    authUser("error", data)
                }
            }
          })
    }



    submitBtn.onclick = (e) => {
        e.preventDefault()
        const inpR = document.querySelectorAll("form input[required]")
        let err = 0
        inpR.forEach(inp => {
            console.log(typeof(inp.value))
            if (inp.value.trim().length == 0) {
                err = 1
                inp.focus()
                return Swal.fire("Lỗi!", "Vui lòng nhập đủ thông tin!", "error")
            }
        })

        if (!err) {
            const data = {
                min_onl_ticket_booking_time: inpR[1].value,
                min_ticket_sale_time: inpR[2].value,
                min_flight_time: inpR[3].value,

            }
            authUser('success',data)
        }
    }