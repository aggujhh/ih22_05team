console.log("forgot_password.js")

document.querySelector(".back_login_btn")
    .addEventListener("click", () => {
        document.querySelector(".back_login").submit();
    })


const get_authentication_code = document.querySelector(".get_authentication_code")
let error_msg
const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;


document.querySelectorAll('#forgot_password [type="text"]')
    .forEach((e, i) => {
        e.addEventListener('focus', function () {
            if (error_msg) {
                document.querySelectorAll('#forgot_password .error_msg')[i].innerHTML = ""
            }
        })
    })


get_authentication_code.addEventListener("click", () => {
    const email = document.querySelector('[name="email"]').value;
    if (email) {
        if (!regex.test(email)) {
            error_msg = "メールアドレスの形式が正しくありません。再入力してください。"
            document.querySelector('.mail_input_box .error_msg').innerHTML = error_msg;
            return
        }
        get_authentication_code.style.background = "#818181"
        get_authentication_code.innerHTML = `認証コードを送信（${count}）`
        let intervalID = setInterval(function () {
            count--
            get_authentication_code.style.pointerEvents = "none"; // クリック無効化
            get_authentication_code.innerHTML = `認証コードを送信（${count}）`
            if (count === 0) {
                count = 10
                get_authentication_code.innerHTML = `認証コードを送信`
                clearInterval(intervalID);
                get_authentication_code.style.background = "#EC7FB1"
                get_authentication_code.style.pointerEvents = "auto";　//無効化解除
            }
        }, 1000)
        $.ajax({
            url: 'http://127.0.0.1:5000/send_email',
            type: 'POST',
            dataType: 'json',
            data: {
                email: email
            },
            success: function (response) {
                // 请求成功时执行的函数
                console.log('Reset successful');
                document.querySelector('[type="hidden"]').value = email
            },
            error: function (xhr, status, error) {
                // 请求失败时执行的函数
                console.error('Error response:', error.response);
                console.error('Error message:', error.message);
            }
        });
    } else {
        error_msg = "メールアドレスは空にできません。再入力してください。"
        document.querySelector('.mail_input_box .error_msg').innerHTML = error_msg;
        return
    }
})