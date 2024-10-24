console.log("script.js");

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

const textBoxs = document.querySelectorAll('[type="text"],[type="password"]')

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



