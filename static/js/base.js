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

short_line.style.left = lis[0].offsetLeft + 'px';
lis.forEach(li => {
    li.addEventListener("click", (e) => {
        e.preventDefault();
        if (e.target.tagName === "LI") {
            short_line.style.left = e.target.offsetLeft + 'px';
        } else {
            short_line.style.left = e.target.closest('li').offsetLeft + 'px';
        }
        console.log(e.target.offsetLeft)
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



