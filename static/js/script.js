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

const inputList = document.querySelectorAll('[type=text]')
inputList.forEach(function (element) {
    element.addEventListener('focus', function () {
        element.classList.add('search')
    })
    element.addEventListener('blur', function () {
        element.classList.remove('search')
    })
});



