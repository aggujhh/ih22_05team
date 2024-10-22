console.log("script.js");

function datejapanese(pubdate) {
    const date = new Date(pubdate);
    const pubdateTxt = date.getFullYear() + "年"
        + (date.getMonth() + 1) + "月"
        + date.getDate() + "日 "
        + date.getHours() + "時"
        + date.getMinutes() + "分"
        + date.getSeconds() + "秒";
    return pubdateTxt;
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

// クローズボッタ
const btn1 = document.querySelector('.close1')
const btn2 = document.querySelector('.close2')
if (btn1) {
    btn1.addEventListener('click', () => btn1.parentNode.style.display = 'none')
} else if (btn2) {
    btn2.addEventListener('click', () => btn2.parentNode.style.display = 'none')
}

// カウントダウンとAjaxリクエストを使って、一定時間後にログインをリセットする処理
const dis_btn = document.querySelector(".dis_btn")
let count = 10
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

