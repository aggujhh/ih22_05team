console.log("base.js");

const logo = document.querySelector("#logo-container")
logo.addEventListener("click", () => window.location.href = '/')


// クローズボッタ
const btn1 = document.querySelector('.close1')
const btn2 = document.querySelector('.close2')
if (btn1) {
    btn1.addEventListener('click', () => btn1.parentNode.style.display = 'none')
} else if (btn2) {
    btn2.addEventListener('click', () => btn2.parentNode.style.display = 'none')
}


const my_page_select = document.querySelector('.my_page_select')
const option_list = $('.option_list');
let hideTimeout;
if (my_page_select) {
    my_page_select.addEventListener('mouseenter', function () {
        clearTimeout(hideTimeout);
        option_list.stop().slideDown();
    });
    my_page_select.addEventListener('mouseleave', function () {
        hideTimeout = setTimeout(function () {
            option_list.stop().slideUp();
        }, 300);
    });
}

const lis = document.querySelectorAll('nav li')
const short_line = document.querySelector('.short_line')
let nav_name;
let left;

lis.forEach(li => {
    li.addEventListener("click", (e) => {
        e.preventDefault();
        if (e.target.tagName === "LI") {
            nav_name = e.target.classList
            left = e.target.offsetLeft + 'px';
            if (short_line) short_line.style.left = left
        } else {
            nav_name = e.target.closest('li').classList
            left = e.target.closest('li').offsetLeft + 'px';
            if (short_line) short_line.style.left = left
        }
        console.log(e.target.offsetLeft)
        document.querySelector('[name="left_margin"]').value = left
        const nav_redirect_form = document.querySelector(".nav_redirect")
        nav_redirect_form.action = `<${nav_name}>`
        if (short_line) {
            setTimeout(function () {
                nav_redirect_form.submit();
            }, 400);
        } else {
            nav_redirect_form.submit();
        }
    })
})

const textBoxs = document.querySelectorAll('[type="text"],[type="password"],textarea')

// テキスト入力チェック
textBoxs.forEach((textBox) => {
    const error_msg = textBox.parentNode.querySelector(".error_msg")
    textBox.addEventListener('focus', function () {
        if (error_msg) {
            error_msg.innerHTML = ""
        }
        textBox.classList.add('pink_border')
    })
    textBox.addEventListener('blur', function () {
        textBox.classList.remove('pink_border')
    })
})


// テキストエリアの入力した文字制限
const textarea = document.querySelector("textarea")
const count_text = document.querySelector('.count_text')

if (textarea) {
    textarea.addEventListener("input", (e) => {
        count_text.innerHTML = `${e.target.value.length}/1200文字`
        if (e.target.value.length > 1200) {
            count_text.style.color = "red"
            textarea.style.color = "red"
            textarea.parentNode.querySelector(".error_msg").innerText = `文字数は1200字を超えてはいけません。`
        } else {
            count_text.style.color = "#818181"
            textarea.style.color = "#111"
            textarea.parentNode.querySelector(".error_msg").innerText = ""
        }

    })
}

const chat_title = document.querySelector("#chat_box .chat_title")
const chars = document.querySelectorAll("#chat_box .chat_title > div")
const first_char = document.querySelector("#chat_box .chat_title > div:first-of-type")
const chat_box = document.querySelector("#chat_box")
const chat_area = document.querySelector("#chat_box .chat_area")
let chat_flag = true

chat_title.addEventListener("click", () => {
    if (chat_flag) {
        chat_box.style.height = "800px"
        setTimeout(function () {
            chat_box.style.width = "400px"
            chat_title.style.transform = "translateX(180px) translateY(-40px) rotate(-90deg)"
        }, 600);
        setTimeout(function () {
            chars.forEach(e => {
                e.style.transform = "rotate(90deg)"
            })
            first_char.style.transform = "rotate(0deg)"
            chat_area.style.opacity = 1
        }, 800);
        chat_flag = false
    } else {
        chat_area.style.opacity = 0
        chat_title.style.transform = "translateX(0) translateY(0) rotate(0)"
        chars.forEach(e => {
            e.style.transform = "rotate(0deg)"
        })
        setTimeout(function () {
            chat_box.style.width = "40px"
        }, 600);
        setTimeout(function () {
            chat_box.style.height = "200px"
        }, 1200);
        chat_flag = true
    }
})


const chat_user_box = document.querySelector("#chat_box .chat_user_box")
const arrow = document.querySelector("#chat_box .chat_user_box_btn")
const chat_user_icon = document.querySelector("#chat_box .chat_user_box img")
const users = document.querySelector("#chat_box .chat_user_box .users")
const add_user = document.querySelector("#chat_box .chat_user_box .add_user")
let chat_user_flag = true
arrow.addEventListener("click", () => {
    if (chat_user_flag) {
        chat_user_box.style.width = "82px"
        chat_user_flag = false
        arrow.innerHTML = "<p>◀</p>"
        chat_user_icon.style.opacity = 0
        users.style.opacity = 1
        add_user.style.opacity = 1
    } else {
        chat_user_box.style.width = "20px"
        chat_user_flag = true
        users.style.opacity = 0
        chat_user_icon.style.opacity = 1
        arrow.innerHTML = "<p>▶</p>"
        add_user.style.opacity = 0
    }
})
const add_user_area = document.querySelector("#chat_box .add_user_area")
document.querySelector("#chat_box .close_btn")
    .addEventListener("click", (e) => {
    add_user_area.style.transform = "translateY(100%)"
})

add_user.addEventListener("click", () => {
    add_user_area.style.transform = "translateY(0)"
})

