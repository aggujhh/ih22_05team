console.log("inquiry.js")

window.addEventListener("load", () => {
    inquiry()
})

function inquiry() {
    const select = document.querySelector('[name="category"]')
    const options = select.children
    const textarea = document.querySelector("textarea")
    const count_text = document.querySelector('.count_text')
    const check_items = document.querySelectorAll('#inquiry [type="text"],#inquiry select,#inquiry textarea')
    const check_btn = document.querySelector(".inquiry_btn")


    select.addEventListener("click", () => {
        options[0].disabled = true
        options[0].style.color = "#818181"
        options[0].style.backgroundColor = "#bbb"
    })

    select.addEventListener("change", () => {
        select.style.color = "#333"
    })

    check_text_count(textarea, count_text, 1200)
    check_input(check_items, check_btn)
}

function check_input(check_items, check_btn) {
    const error_msg_list = document.querySelectorAll(".error_msg")
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const inquiry_form = document.querySelector("#inquiry_form")

    check_btn.addEventListener("click", () => {
        const text_length = document.querySelector("textarea").value.length
        console.log(text_length)
        check_items.forEach((e, i) => {
            console.log("i" + i)
            if (!emailRegex.test(e.value) && i === 1) {
                error_msg_list[i].innerHTML = `${e.dataset.name}の形式が正しくありません。再入力してください。`
            } else if (!e.value && i === 2) {
                error_msg_list[i].innerHTML = `${e.dataset.name}を選択してください`
            } else if (text_length > 1200 && i === 3) {
                error_msg_list[i].innerHTML = `文字数は1200字を超えてはいけません。`
            } else if (!e.value) {
                error_msg_list[i].innerHTML = `${e.dataset.name}を入力してください`
            } else {
                error_msg_list[i].innerHTML = ""
                inquiry_form.submit()
            }
        })
    })
}

