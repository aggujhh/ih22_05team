console.log("login.js");

window.addEventListener("load", function () {
    reset_time_down()
})


function reset_time_down() {
    // カウントダウンとAjaxリクエストを使って、一定時間後にログインをリセットする処理
    let mail_address
    const dis_btn = document.querySelector(".dis_btn")
    const mail = document.querySelector('.login [type="hidden"]')
    if (mail) mail_address = mail.value
    let count = 3
    if (dis_btn) {
        dis_btn.innerHTML = `ログイン(${count})`
        let intervalID = setInterval(function () {
            count--
            dis_btn.innerHTML = `ログイン(${count})`
            if (count === 0) {
                clearInterval(intervalID);
                $.ajax({
                    url: 'http://127.0.0.1:5000/reset',
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        mail: mail_address
                    },
                    success: function (response) {
                        // 请求成功时执行的函数
                        console.log('Reset successful');
                        window.location.href = '/redirect_to_login';
                    },
                    error: function (xhr, status, error) {
                        // 请求失败时执行的函数
                        console.error('Error response:', error.response);
                        console.error('Error message:', error.message);
                    }
                });
            }
        }, 1000)
    }
}


