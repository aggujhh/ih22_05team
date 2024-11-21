console.log("base.js");

window.addEventListener("load", function () {
    const left_margin = document.querySelectorAll('header nav li')[0].offsetLeft + 'px'
    const short_line = document.querySelector(".short_line")
    if (short_line.style.left === "0px") {
        short_line.style.left = left_margin
    }
})

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

const lis = document.querySelectorAll('header nav li')
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
        nav_redirect_form.action = `/${nav_name}`
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
const textarea = document.querySelector("#creator_form textarea")
const count_text = document.querySelector('.count_text')

function check_text_count(textarea, count_text, max) {
    if (textarea) {
        textarea.addEventListener("input", (e) => {
            count_text.innerHTML = `${e.target.value.length}/${max}文字`
            if (e.target.value.length > max) {
                count_text.style.color = "red"
                textarea.style.color = "red"
                textarea.parentNode.querySelector(".error_msg").innerText = `文字数は${max}字を超えてはいけません。`
            } else {
                count_text.style.color = "#818181"
                textarea.style.color = "#111"
                textarea.parentNode.querySelector(".error_msg").innerText = ""
            }
        })
    }
}

check_text_count(textarea, count_text, 1200)


const new_request_btn = document.querySelector(".new_request_btn")
if (new_request_btn) {
    new_request_btn.addEventListener("click", () => {
        console.log("new_request_btn click")
        localStorage.clear();
        let progress_value_list = {
            bar_width: 10,
            kapibara_move: 0,
            star_boxes_index: 0
        };

        // let new_request_list = {}
        localStorage.setItem("progress_value_list", JSON.stringify(progress_value_list))
        // localStorage.setItem("new_request_list", JSON.stringify(new_request_list))
        new_request_btn.parentNode.submit();
    })
}


function set_toggle() {
    const slider = document.querySelector(".slider")
    const toggle_switch = document.querySelector(".toggle_switch")
    toggle_switch.addEventListener("click", (e) => {
        toggle_switch.classList.toggle("off")
        slider.classList.toggle("left")
    })
}


function check_box() {
    const checkAll = document.querySelector('#checkAll')
    const cks = document.querySelectorAll('.ck')
    if (checkAll) {
        checkAll.checked = cks.length === document.querySelectorAll('.ck:checked').length
        checkAll.addEventListener('click', function () {
            for (let i = 0; i < cks.length; i++) {
                cks[i].checked = this.checked
            }
        })

        for (let i = 0; i < cks.length; i++) {
            cks[i].addEventListener('click', function () {
                checkAll.checked = cks.length === document.querySelectorAll('.ck:checked').length
            })
        }
    }
}

function add_and_delete_images() {
    // 画像追加かつ表示
    const fileInput = document.querySelector('[type="file"]');  // ファイル入力要素を取得
    const preview_area = document.querySelector(".preview_area");  // 画像プレビューエリアを取得
    let preview_area_temp
    if (preview_area) {
        preview_area_temp = preview_area.innerHTML;  // プレビューエリアの初期状態を保存
    }
    let imagesArray = [];  // 画像データを保存するための配列

    // ファイルが選択された時のイベントリスナー
    if (fileInput) {
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];  // 最初に選択されたファイルを取得
            if (file) {
                if (validateImages(file)) return//画像の形式とサイズが違う場合
                const reader = new FileReader();  // FileReaderを使用してファイルを読み込む
                reader.onload = function (e) {
                    imagesArray.push(e.target.result);  // 画像データを配列に追加
                    updatePreview(preview_area_temp);  // プレビューを更新
                };
                reader.readAsDataURL(file);  // ファイルをData URLとして読み込む
            }
        });
    }


    // プレビューエリアを更新する関数
    function updatePreview(preview_area_temp) {
        preview_area.innerHTML = preview_area_temp;  // プレビューエリアを初期状態に戻す
        for (let index = 0; index < imagesArray.length; index++) {
            const imageData = imagesArray[index];
            const children = preview_area.children;
            // 获取倒数第二个元素
            const target = children[children.length - 1];
            target.insertAdjacentHTML('beforebegin',
                `<div class="preview" style="background-image:url(${imageData})">
                <button class="close_btn">✖</button>
            </div>`
            );
        }
    }

    preview_area.addEventListener('click', (event) => {
        console.log(imagesArray)
        if (event.target.classList.contains('close_btn')) {
            const parent = event.target.parentNode; // 获取按钮的父节点
            const imageUrl = parent.style.backgroundImage; // 获取父节点的背景图片
            // 提取背景图片的 URL（去掉 'url("...")' 的包装）
            const imageData = imageUrl.slice(5, -2);
            // 找到对应图片在 imagesArray 中的索引
            const index = imagesArray.indexOf(imageData);
            if (index >= 0) {
                imagesArray.splice(index, 1); // 从 imagesArray 中移除对应的图片数据
                console.log(imagesArray)
                parent.remove();
            }
            // preview_area_temp = preview_area.innerHTML

        } else if (event.target.classList.contains("delete_btn")) {
            const image_name = event.target.dataset.name
            console.log("image_name", image_name)
            $.ajax({
                url: 'http://127.0.0.1:5000/delete_image',
                type: 'POST',
                dataType: 'json',
                data: {
                    image_name
                },
                success: (response) => {
                    alert(response.message)
                    event.target.parentNode.parentNode.removeChild(event.target.parentNode);
                    const tempContainer = document.createElement('div');
                    tempContainer.innerHTML = preview_area.innerHTML; // 加载缓存内容

                    let child = tempContainer.lastElementChild;
                    for (let i = 0; i < imagesArray.length && child; i++) {
                        const toRemove = child.previousElementSibling; // 获取倒数第二个子元素
                        if (toRemove) {
                            tempContainer.removeChild(toRemove); // 删除目标子元素
                        }
                        child = child.previousElementSibling; // 更新指针
                    }


                    // 更新 preview_area_temp
                    preview_area_temp = tempContainer.innerHTML;
                },
                error: function (xhr, status, error) {
                    // 请求失败时执行的函数
                    console.error('Error response:', error.response);
                    console.error('Error message:', error.message);
                }
            });
        }
    });


    //画像の形式とサイズをチェックする
    function validateImages(image) {
        preview_area.nextElementSibling.innerHTML = ""
        const maxSize = 2 * 1024 * 1024;  // 最大2MB
        const allowedFormats = ['image/jpeg', 'image/png', 'image/jpg'];  // 許可される画像形式
        let count = 0
        // 画像形式をチェック
        if (!allowedFormats.includes(image.type)) {
            console.log(image.type)
            preview_area.nextElementSibling.innerHTML += "サポートされていない画像形式です。JPEG、PNG、jpg形式のみ使用可能です。<br>"
            count++
        }
        // 画像サイズをチェック
        if (image.size > maxSize) {
            preview_area.nextElementSibling.innerHTML += "画像サイズが2MBの制限を超えています。"
            count++
        }
        return count !== 0
    }

    return imagesArray
}

function throttle(func, wait) {
    let timeout = null;
    return function () {
        if (!timeout) {
            timeout = setTimeout(() => {
                func.apply(this);
                timeout = null;
            }, wait);
        }
    };
}