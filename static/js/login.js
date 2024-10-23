console.log("login.js");

// カウントダウンとAjaxリクエストを使って、一定時間後にログインをリセットする処理
const dis_btn = document.querySelector(".dis_btn")
let count = 10
if (dis_btn) {
    dis_btn.innerHTML = `ログイン(${count})`
    let intervalID = setInterval(function () {
        count--
        dis_btn.innerHTML = `ログイン(${count})`
        if (count === 0) {
            clearInterval(intervalID);
            $.ajax({
                url: 'http://127.0.0.1:5000/reset',
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

// テキストボックスのborder色チェンジ
const inputList = document.querySelectorAll('[type=text]')
inputList.forEach(function (element) {
    element.addEventListener('focus', function () {
        element.classList.add('search')
    })
    element.addEventListener('blur', function () {
        element.classList.remove('search')
    })
});