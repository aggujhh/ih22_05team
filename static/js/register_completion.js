console.log("register_completion.js");

let redirect = document.querySelector('.register_completion small')
let count = 5
redirect.innerText = `※${count}秒後に自動「COSBARA」トップページへ遷移します。遷移しない場合は、下のボタンをクリックしてください。`
let timerId = setInterval(function () {
    count--
    redirect.innerText = `※${count}秒後に自動「COSBARA」トップページへ遷移します。遷移しない場合は、下のボタンをクリックしてください。`
    if (count === 0) {
        clearInterval(timerId)
        location.href = 'http://127.0.0.1:5000/'
    }
}, 1000)