console.log("requests.js")
let initialCall = true;

function throttle(func, wait) {
    let timeout = null;
    return function () {
        if (initialCall) {
            func.apply(this); // 第一次立即调用
            initialCall = false;
        }
        if (!timeout) {
            timeout = setTimeout(() => {
                func.apply(this);
                timeout = null;
            }, wait);
        }
    };
}


const windows_scroll = throttle(() => {
    let load_count = 0
    // 現在のウィンドウの下端位置とリストの下端位置をログに出力
    console.log(window.scrollY + window.innerHeight, request_list.offsetTop + request_list.offsetHeight);
    // ウィンドウの下端の位置を計算
    let window_bottom = window.scrollY + window.innerHeight;
    // リストの下端の位置を計算 (160ピクセルの余裕を追加)
    let request_list_bottom = request_list.offsetTop + request_list.offsetHeight + 160;
    // ウィンドウの下端がリストの下端を超えた場合、"ページ触底了"を表示
    if (window_bottom >= request_list_bottom) {
        load_count++
        loader.style.display = "block";
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
                console.log('Reset successful');
            },
            error: function (xhr, status, error) {
                // 请求失败时执行的函数
                console.error('Error response:', error.response);
                console.error('Error message:', error.message);
            }
        });
        // setTimeout(function () {
        //     request_list.innerHTML += `<li class="request_box"></li>
        //                         <li class="request_box"></li>
        //                         <li class="request_box"></li>
        //                         <li class="request_box"></li>`
        // }, 1000);
    } else {
        loader.style.display = "none";
    }
}, 1000);

const request_list = document.querySelector(".request-list ul")
const loader = document.querySelector("#requests_view .loader")
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

const request_boxes = document.querySelectorAll(".request_box")
const get_request_id = document.querySelector(".get_request_id")

request_boxes.forEach(request => {
    console.log(request)
    request.addEventListener("click", (e) => {
        const targetElement = e.target.closest("[data-id]");
        if (targetElement) {
            get_request_id.action = `/request/${targetElement.dataset.id}`
            get_request_id.submit();
        }
    })
})

