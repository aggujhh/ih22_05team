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
        chat_interface.style.display = "none"
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

const first_u = document.querySelector("#chat_box .chat_user_box  li:first-of-type")
const first_c = document.querySelector("#chat_box .channel_area  li:first-of-type")
const chat_interface = document.querySelector(" #chat_box .chat_interface")

first_u.addEventListener("click", () => {
    chat_interface.style.display = "flex"
    document.querySelector("")
})

first_c.addEventListener("click", () => {
    chat_interface.style.display = "flex"
})

document.querySelector(".chat_interface_header p:first-of-type")
    .addEventListener("click", () => {
        chat_interface.style.display = "none"
    })


// チャットの入力欄の設定
const input_textarea = document.querySelector('.chat_input_box>textarea ')
let temp_height
input_textarea.addEventListener('input', function () {
    // this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
    temp_height = this.scrollHeight + 'px';
});

input_textarea.addEventListener('focus', function () {
    console.log(input_textarea.value)
    if (input_textarea.value === "") {
        console.log(123)
        this.style.height = "30px";
    } else {
        this.style.height = temp_height;
    }
})
input_textarea.addEventListener("blur", () => {
    input_textarea.style.height = "30px"
})


// チャットの入力欄の入力動作
document.querySelector(".chat_input_box div").addEventListener("click", function (e) {
    const imgSrc = "../static/img/cyonncyonn2.svg";
    const currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

    const chatContent = document.querySelector(".chat_interface_content ul")
    chatContent.insertAdjacentHTML('beforeend', `
                <li>
                    <div class="sentMessage">
                        <p>${input_textarea.value}</p>
                        <img src="${imgSrc}">
                        <p>${currentTime}</p>
                    </div>
                </li>`);
    input_textarea.value = "";
    chatContent.lastElementChild.scrollIntoView({behavior: "smooth"});
})

