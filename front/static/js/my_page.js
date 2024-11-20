console.log("my_page.js")

const imagesArray = {}
const article = document.querySelector("article")

window.addEventListener("load", () => {
    if (article.id === "profile_Settings") {
        my_page2()
    } else if (article.id === "production_management") {
        my_page9()
    }
})

function my_page2() {
    const upload_bg_img = document.querySelector("#upload_bg_img")
    const upload_picture = document.querySelector("#upload_picture")
    const upload_bg_img_btn = document.querySelector(".bg_img button")
    const upload_picture_btn = document.querySelector(".picture button")
    const bg_img = document.querySelector(".bg_img")
    const picture = document.querySelector(".picture>div>div")
    const submit_btn = document.querySelector(".submit_btn")
    const update_profile = document.querySelector("#update_profile")

    // bg_img.style.backgroundColor = "#d9d9d9"
    // picture.style.backgroundColor = "#d9d9d9"

    upload_bg_img_btn.addEventListener("click", () => {
        upload_bg_img.click()
    })

    upload_picture_btn.addEventListener("click", () => {
        upload_picture.click()
    })

    upload_bg_img.addEventListener("change", (event) => {
        const img_type = "background_photo_url"
        const img_data = event.target.files[0]
        if (validateImages(img_data)) return
        upload_image(img_type, img_data)
            .then(result => {
                imagesArray[img_type] = result
                displayImage(bg_img, result)
            })
            .catch(error => console.error(error));
    })

    upload_picture.addEventListener("change", (event) => {
        const img_type = "icon_url"
        const img_data = event.target.files[0]
        if (validateImages(img_data)) return
        upload_image(img_type, img_data)
            .then(result => {
                imagesArray[img_type] = result
                displayImage(picture, result)
            })
            .catch(error => console.error(error));
    })

    const textarea1 = document.querySelector('[name="profile"]')
    const textarea2 = document.querySelector('[name="hobby"]')
    const count_text = document.querySelectorAll('.count_text')

    check_text_count(textarea1, count_text[0], 1200)
    check_text_count(textarea2, count_text[1], 800)


    submit_btn.addEventListener("click", () => {
        count = 0
        if (textarea1.value.length > 1200) {
            count_text[0].nextElementSibling.innerHTML = "文字数は1200字を超えてはいけません。"
            count++
        } else {
            count_text[0].nextElementSibling.innerHTML = ""
        }
        if (textarea2.value.length > 800) {
            count_text[1].nextElementSibling.innerHTML = "文字数は800字を超えてはいけません。"
            count++
        } else {
            count_text[1].nextElementSibling.innerHTML = ""
        }

        if (count === 0) {
            $.ajax({
                url: 'http://127.0.0.1:5000/update_profile_images',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({imagesArray}),
                success: function (response) {
                    // 请求成功时执行的函数
                    console.log('Reset successful');
                    alert(response.message)
                    update_profile.submit()
                },
                error: function (xhr, status, error) {
                    // 请求失败时执行的函数
                    console.error('Error response:', error.response);
                    console.error('Error message:', error.message);
                }
            });
        }
    })
}

function upload_image(img_type, file) {
    return new Promise((resolve, reject) => {
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imagesArray[img_type] = e.target.result;  // 保存图片数据
                resolve(e.target.result);  // 成功时返回结果
            };
            reader.onerror = function () {
                console.error("文件读取出错");
                reject("文件读取出错");
            };
            reader.readAsDataURL(file);
        } else {
            reject("没有文件传入");
        }
    });
}


function displayImage(area, dataUrl) {
    area.style.backgroundImage = `url(${dataUrl})`
}

function validateImages(image) {
    const maxSize = 2 * 1024 * 1024;  // 最大2MB
    const allowedFormats = ['image/jpeg', 'image/png', 'image/jpg'];  // 許可される画像形式
    let errorMessage = "";

    // 画像形式をチェック
    if (!allowedFormats.includes(image.type)) {
        console.log(image.type)
        errorMessage += "サポートされていない画像形式です。JPEG、PNG、jpg形式のみ使用可能です。\\n"
    }
    // 画像サイズをチェック
    if (image.size > maxSize) {
        errorMessage += "画像サイズが2MBの制限を超えています。"
    }
    if (errorMessage) {
        alert(errorMessage)
        return true
    }
    return false
}

function my_page9() {
    const navs = document.querySelectorAll("#production_management >nav >div")
    const request_availability = document.querySelector('[name="request_availability"]')
    const toggle_switch = document.querySelector('.toggle_switch')
    const next_step_btn = document.querySelector('.next_step_btn')
    const images_input = document.querySelector('[name="image"]')
    navs.forEach((e, i) => {
        if (i !== 0) {
            e.addEventListener("click", () => {
                window.location.href = `/my_page/9/${i}`;
            })
        }
    })

    set_toggle()
    check_box()
    let imagesArray = add_and_delete_images()
    next_step_btn.addEventListener("click", () => {
        const preview = document.querySelector(".preview")
        if (toggle_switch.classList.contains("off")) {
            request_availability.value = "0"
        } else {
            request_availability.value = "1"
        }
        get_expertise_list_data()
        images_input.value = JSON.stringify({images: imagesArray})
        console.log(images_input.value)



        document.querySelector("#creator_setting_form").submit()
    })


}

function get_expertise_list_data() {
    let list = [0, 0, 0, 0, 0, 0]
    const cks = document.querySelectorAll('.ck')
    for (let i = 0; i < cks.length; i++) {
        if (cks[i].checked) {
            list[i] = 1
        }
    }
    document.querySelector('[name="expertise"]').value = JSON.stringify(list)
}


// function delete_image() {
//     const preview_area = document.querySelector(".preview_area");
//     // const delete_btn = document.querySelectorAll(".delete_btn")
//     preview_area.addEventListener("click", function (event) {
//
//     })
// }

