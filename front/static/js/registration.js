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
            },
            error: function (xhr, status, error) {
                // 请求失败时执行的函数
                console.error('Error response:', error.response);
                console.error('Error message:', error.message);
            }
        });
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
const inputs = document.querySelectorAll('#requester_form li>input,#creator_form li>input,textarea')
const requester_btn = document.querySelector(".requester_btn")
const creator_btn = document.querySelector(".creator_btn")
const checkBox = document.querySelector('[type="checkbox"]')


function not_full() {
    let count = 0
    inputs.forEach((e, i) => {
        if (e.value === "") {
            if (e.dataset.name === "制作物画像") {
                e.parentNode.querySelector(".error_msg").innerText = `少なくとも1枚の制作物画像をアップロードしてください。`
            } else {
                if (e.dataset.name) {
                    e.parentNode.querySelector(".error_msg").innerText = `${e.dataset.name}は空にできません。再入力してください。`
                }
            }
        } else {
            count++
        }
    })
    console.log(count, inputs.length)
    return count < inputs.length - 1
}

if (requester_btn) {
    requester_btn.addEventListener(("click"), () => {
        console.log(!not_full())
        if (checkBox.checked && !not_full()) {
            document.querySelector("#requester_form").submit();
        } else {
            if (!checkBox.checked) {
                checkBox.parentNode.parentNode.querySelector(".error_msg").innerText = `利用規約をよくお読みの上、確認ボタンをクリックしてください。`
            }
            requester_btn.classList.add("dis_btn")
        }
    })
}


checkBox.addEventListener("click", (e) => {
    if (e.target.checked) {
        checkBox.parentNode.parentNode.querySelector(".error_msg").innerText = ""
    }
    if (e.target.checked && !not_full()) {
        if (requester_btn) requester_btn.classList.remove("dis_btn")
        if (creator_btn) creator_btn.classList.remove("dis_btn")
    } else {
        if (requester_btn) requester_btn.classList.add("dis_btn")
        if (creator_btn) creator_btn.classList.add("dis_btn")
    }
})

const creator_image = document.querySelector('[name="image"]')
const imagesArray = add_and_delete_images()

if (creator_btn) {
    creator_btn.addEventListener(("click"), () => {
        console.log(!not_full())
        if (checkBox.checked && !not_full()) {
            console.log("OK")
            $.ajax({
                url: 'http://127.0.0.1:5000/upload_img',
                type: 'POST',
                contentType: 'application/json',  // 送信するデータの種類をJSONに設定
                dataType: 'json',
                data: JSON.stringify({images: imagesArray}),  // オブジェクト全体をJSON文字列に変換
                success: function (response) {
                    // 请求成功时执行的函数
                    console.log('Reset successful');
                    console.log(response.urls)
                    creator_image.value = JSON.stringify(response.urls);
                    document.querySelector("#creator_form").submit();
                },
                error: function (xhr, status, error) {
                    // 请求失败时执行的函数
                    console.error('Error response:', error.response);
                    console.error('Error message:', error.message);
                }
            });
            // document.querySelector("#requester_form").submit();
        } else {
            if (!checkBox.checked) {
                checkBox.parentNode.parentNode.querySelector(".error_msg").innerText = `利用規約をよくお読みの上、確認ボタンをクリックしてください。`
            }
            creator_btn.classList.add("dis_btn")
        }
    })

}
