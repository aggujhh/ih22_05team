console.log(registration.js)


const user_types = document.querySelectorAll('[name="user_type"]')
const myForm = document.querySelector('#myForm')
const user_type_data = document.querySelector('[name="user_type_data"]')

user_types.forEach(user_type => {
    console.log(user_type.value)
    user_type.addEventListener("change", () => {
        user_type_data.value = user_type.value
        myForm.submit();
    })
})


const get_authentication_code = document.querySelector(".get_authentication_code")
let error_msg
let count = 10
get_authentication_code.innerHTML = `認証コードを取得する（${count}）`
const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
get_authentication_code.addEventListener("click", () => {
    const email = document.querySelector('[name="email"]').value;
    if (email) {
        if (!regex.test(email)) {
            error_msg = "メールアドレスの形式が正しくありません。再入力してください。"
            document.querySelector('main li:nth-of-type(2)>small').innerHTML = error_msg;
            return
        }
        document.querySelector('[action="/send_email"] [name="email"]').value = email
        document.querySelector('[action="/send_email"]').submit();
    } else {
        error_msg = "メールアドレスは空にできません。再入力してください。"
        document.querySelector('main li:nth-of-type(2)>small').innerHTML = error_msg;
        return
    }
    get_authentication_code.style.color = "#818181"
    let intervalID = setInterval(function () {
        count--
        get_authentication_code.innerHTML = `認証コードを取得する（${count}）`
        get_authentication_code.style.pointerEvents = "none"; // クリック無効化
        if (count === 0) {
            count = 10
            get_authentication_code.innerHTML = `認証コードを取得する（${count}）`
            clearInterval(intervalID);
            get_authentication_code.style.color = "#FF3578"
            get_authentication_code.style.pointerEvents = "auto";　//無効化解除
        }
    }, 1000)
})

// アカウント作成したフォームの正解性チェック
const registration_inputs = document.querySelectorAll('#requester_form [type="text"],#requester_form [type="password"]')
const registration_err_list = ["ニックネーム", "メールアドレス", "メール認証コード", "パスワード", "パスワード確認"]
const requester_btn = document.querySelector(".requester_btn")
const requester_checkBox = document.querySelector('[type="checkbox"]')

function not_full() {
    let count = 0
    registration_inputs.forEach((e, i) => {
        if (e.value === "") {
            e.parentNode.querySelector(".error_msg").innerText = `${registration_err_list[i]}は空にできません。再入力してください。`
        } else {
            count++
        }
    })
    return count < registration_err_list.length
}

requester_btn.addEventListener(("click"), () => {
    console.log(!not_full())
    if (requester_checkBox.checked && !not_full()) {
        document.querySelector("#requester_form").submit();
    } else {
        if (!requester_checkBox.checked) {
            requester_checkBox.parentNode.parentNode.querySelector(".error_msg").innerText = `利用規約をよくお読みの上、確認ボタンをクリックしてください。`
        }
        requester_btn.classList.add("dis_btn")
    }
})
requester_checkBox.addEventListener("click", (e) => {
    if(e.target.checked){
         requester_checkBox.parentNode.parentNode.querySelector(".error_msg").innerText =""
    }
    if (e.target.checked && !not_full()) {
        requester_btn.classList.remove("dis_btn")
    } else {
        requester_btn.classList.add("dis_btn")
    }
})

