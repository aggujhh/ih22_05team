console.log("creators.js")

window.addEventListener("load", function () {
    const windows_scroll = load_creator()
    window.addEventListener("scroll", windows_scroll)
})

function load_creator() {
    let load_count = 0
    let load_flag = true
    const creators_list = document.querySelector(".creators-list")

    const windows_scroll = throttle(() => {
        // ウィンドウの下端の位置を計算
        let window_bottom = window.scrollY + window.innerHeight;
        // リストの下端の位置を計算 (160ピクセルの余裕を追加)
        let request_list_bottom = creators_list.offsetTop + creators_list.offsetHeight + 160;
        // ウィンドウの下端がリストの下端を超えた場合、"ページ触底了"を表示
        if (window_bottom >= request_list_bottom && load_flag) {
            load_count++
            console.log("ページの下端に到達しました");
            $.ajax({
                url: 'http://127.0.0.1:5000/load_new_creators',
                type: 'POST',
                dataType: 'json',
                data: {
                    load_count
                },
                success: function (response) {
                    // 请求成功时执行的函数
                    console.log(response.message, response.data)
                    const creators_list = document.querySelector(".creators-list >ul")
                    if (!response.data) {
                        load_flag = false
                        creators_list.innerHTML += "<p>すべての制作者はこちらで以上となります。</p>"
                        console.log("Loader should be hidden now");
                        return
                    }
                    response.data.forEach(e => {
                        let request_availability
                        if (e.request_availability == "0") {
                            request_availability = `<div class="stop_temporarily">
                                                        <p>制作一時停止</p>
                                                        <div class="triangle"></div>
                                                    </div>`
                        } else {
                            request_availability = `<div>
                                                        <p>制作可能</p>
                                                        <div class="triangle"></div>
                                                    </div>`
                        }

                        let gender=""
                        if (e.gender == "1") {
                            gender = `<div class="user_gender" style="color: #43AEF5">♂</div>`
                        } else if (e.gender == "2") {
                            gender = `<div class="user_gender">♀</div>`
                        }

                        let category_stages_list = ""
                        if (e.category_stages) {
                            e.category_stages.forEach((item, i) => {
                                if (item === "1") {
                                    category_stages_list += `
                                <div class="tag"
                                     style="background: ${e.category_colors[i]}">${e.category_names[i]}</div>
                                `
                                }
                            })
                        }


                        let images_list = ""
                        if (e.images_list) {
                            e.images_list.forEach((item) => {
                                images_list += `<div><img src="../static${item}"></div>`
                            })
                        }

                        creators_list.innerHTML += `<li class="creator_box">
                            <div class="user_icon_box">
                                ${request_availability}
                                <div class="user_icon"
                                     style="background-image: url('../static/${e.icon_path}')">
                                    <img src='../static/img/gold.svg'">
                                </div>
                            </div>
                            <div class="user_content">
                                <div>
                                    <div class="user_name">
                                        ${e.nickname}
                                        ${gender}
                                    </div>
                                    <div class="evaluation_box">
                                        <div class="star-rating" title="70%">
                                            <div class="back-stars">
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                <i class="fa fa-star"></i>
                                                <div class="front-stars" style="width: 70%">
                                                    <i class="fa fa-star"></i>
                                                    <i class="fa fa-star"></i>
                                                    <i class="fa fa-star"></i>
                                                    <i class="fa fa-star"></i>
                                                    <i class="fa fa-star"></i>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="point">4.5</div>
                                    </div>
                                    <div class="req_count">制作件数：18</div>
                                </div>
                                <div class="strong_field">
                                    得意分野
                                ${category_stages_list}
                                </div>
                                <div class="profile">
                                    ${e.creator_notification}
                                </div>
                                <form action="/creator/${e.user_id}" method="post">
                                    <button>プロフィールを見る</button>
                                </form>
                            </div>
                            <div class="user_img">${images_list}</div>
                        </li>`
                    })
                    // add_creator_redirect()
                },
                error: function (xhr, status, error) {
                    // 请求失败时执行的函数
                    console.error('Error response:', error.response);
                    console.error('Error message:', error.message);
                }
            });
        }
    }, 400);
    return windows_scroll
}



