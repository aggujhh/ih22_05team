console.log("requests.js")


let load_count = 0
let load_flag = true
const windows_scroll = throttle(() => {
    // ウィンドウの下端の位置を計算
    let window_bottom = window.scrollY + window.innerHeight;
    // リストの下端の位置を計算 (160ピクセルの余裕を追加)
    let request_list_bottom = request_list.offsetTop + request_list.offsetHeight + 160;
    // ウィンドウの下端がリストの下端を超えた場合、"ページ触底了"を表示
    if (window_bottom >= request_list_bottom && load_flag) {
        load_count++
        console.log("ページの下端に到達しました");
        $.ajax({
            url: 'http://127.0.0.1:5000/load_new_requests',
            type: 'POST',
            dataType: 'json',
            data: {
                load_count
            },
            success: function (response) {
                // 请求成功时执行的函数
                console.log(response.message, response.data)
                const request_list = document.querySelector(".request-list >ul")
                if (!response.data) {
                    load_flag = false
                    request_list.innerHTML += "<p>すべてのご依頼はこちらで以上となります。</p>"
                    console.log("Loader should be hidden now");
                    return
                }
                response.data.forEach(e => {
                    let request_status
                    if (e.request_status == "0") {
                        request_status = "<div class='request_statu'>制作者募集中</div>"
                    } else if (e.request_status == "1") {
                        request_status = "<div className='request_statu'>制作中</div>"
                    } else {
                        request_status = "<div className='request_statu'>成約完了</div>"
                    }

                    const categories = e.categories
                        .slice(0, 3) // 只取前三个
                        .map((category, index) => {
                            // 第三个显示为 "..."
                            return index === 2 ? `<p>...</p>` : `<p>${category}</p>`;
                        })
                        .join('');
                    request_list.innerHTML += `<li class="request_box" data-id="${e.request_id}">
                        <div class="request_img"
                             style="background-image: url('${e.image_path}')">
                            <div class="request_text">
                                <p class="request_title">
                                    ${e.request_title}</p>
                                <p class="request_time">納期希望　${e.request_deadline}まで</p>
                            </div>
                        </div>
                        ${request_status}
                        <div class="request_category">
                            ${categories}
                        </div>
                        <button class="apply_btn">応募する</button>
                    </li>`
                })
                add_redirect()
            },
            error: function (xhr, status, error) {
                // 请求失败时执行的函数
                console.error('Error response:', error.response);
                console.error('Error message:', error.message);
            }
        });
    }
}, 400);

const request_list = document.querySelector(".request-list ul")
// ウィンドウのスクロールイベントを監視
window.addEventListener("scroll", windows_scroll)


const order = document.querySelector("#requests_view .filter-options .order")

order.addEventListener("click", () => {
    order.children[0].classList.toggle("rotate");
})


const checkAll = document.querySelector('#checkAll')
const cks = document.querySelectorAll('.ck')
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


function add_redirect() {
    const get_request_id = document.querySelector(".get_request_id");

    // 使用事件委托，避免重复绑定事件
    document.querySelector(".request-list > ul").addEventListener("click", (e) => {
        const targetElement = e.target.closest(".request_box[data-id]");
        if (targetElement && get_request_id) {
            get_request_id.action = `/request/${targetElement.dataset.id}`;
            get_request_id.submit();
        }
    });
}

add_redirect()
