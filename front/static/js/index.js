console.log("index.js");

const carousel_left_btn = document.querySelector(".carousel_button_left");
const carousel_right_btn = document.querySelector(".carousel_button_right");
const dot = document.querySelectorAll(".dot");
const carousel_imgs = document.querySelector(".carousel_imgs");
const carousel_box = document.querySelector(".carousel");

let index = 0;
let time = 0;

window.addEventListener("load", () => {
    pause_and_play_the_carousel()
    add_redirect()
    creators_paging()
})


//结合index定义图片位置
function position() {
    carousel_imgs.style.left = (index * -100) + "%";
    refreshDot();
}


position()
refreshDot();


function add() {
    if (index >= (dot.length - 1)) {
        carousel_imgs.style.transition = "0s";
        carousel_imgs.style.left = 0 + "%";
        index = 0
        setTimeout(() => {
            carousel_imgs.style.transition = "";
            index++
            carousel_imgs.style.left = -100 + "%";
            refreshDot()
        }, 40)
    } else {
        index++
        carousel_imgs.style.transition = "";
        position();
    }
}

function desc() {
    if (index === 0) {
        carousel_imgs.style.transition = "0s";
        carousel_imgs.style.left = ((dot.length - 1) * -100) + "%";
        index = (dot.length - 1)
        setTimeout(() => {
            carousel_imgs.style.transition = "";
            index--
            carousel_imgs.style.left = ((dot.length - 2) * -100) + "%";
            refreshDot()
        }, 40)
    } else {
        index--
        carousel_imgs.style.transition = "";
        position();
    }
}

//图片自动播放
function timer() {
    time = setInterval(() => {
        add();
        // position();
    }, 4000)
}

//点击左键
carousel_left_btn.addEventListener("click", () => {
    desc();
})
//点击右键
carousel_right_btn.addEventListener("click", () => {
    add();
    // position();
})

//更新圆点按钮
function refreshDot() {
    dot[(dot.length - 1)].style.display = 'none';
    for (let j = 0; j < dot.length; j++) {
        dot[j].style.backgroundColor = ''
    }
    dot[index].style.backgroundColor = "#fff";
    if (index === dot.length - 1) {
        dot[0].style.backgroundColor = "#fff";
    }
}


//圆点按钮
for (let i = 0; i < dot.length; i++) {
    dot[i].addEventListener("click", () => {
        for (let j = 0; j < dot.length; j++) {
            dot[j].style.backgroundColor = '';

        }
        dot[i].style.backgroundColor = "#fff";
        index = i;
        position();
        clearInterval(time);
        timer();
    })
}


// 添加鼠标移入事件监听器到轮播图区域
carousel_box.addEventListener("mouseover", () => {
    clearInterval(time); // 暂停轮播
});
// 添加鼠标移出事件监听器到轮播图区域
carousel_box.addEventListener("mouseleave", () => {
    timer(); // 继续轮播
});

timer();


function pause_and_play_the_carousel() {
    const requests_box = document.querySelector("#requests_box ul")
    requests_box.addEventListener("mouseover", () => {
        requests_box.style.animationPlayState = "paused";
    });
// 添加鼠标移出事件监听器到轮播图区域
    requests_box.addEventListener("mouseleave", () => {
        requests_box.style.animationPlayState = "running";
    });
}

function add_redirect() {
    console.log("add_redirect")
    const get_request_id = document.querySelector(".get_request_id");

    // 使用事件委托，避免重复绑定事件
    document.querySelector("#requests_box ul").addEventListener("click", (e) => {
        const targetElement = e.target.closest("li[data-id]");
        console.log("targetElement", targetElement)
        if (targetElement && get_request_id) {
            console.log("click ")
            get_request_id.action = `/request/${targetElement.dataset.id}`;
            get_request_id.submit();
        }
    });
}

function creators_paging() {
    const paging_box = document.querySelector(".paging_box");
    let pages = document.querySelectorAll(".paging_box .page");
    const last_page = Number(pages[pages.length - 1].innerHTML)

    // 初始绑定事件
    bindEvents();

    function bindEvents() {
        // 给所有分页按钮绑定点击事件
        pages.forEach((e) => {
            e.addEventListener("click", () => {
                pages.forEach((page) => {
                    page.classList.remove("current");
                });
                e.classList.add("current");
                load_new_creator(Number(e.innerHTML) - 1)
            });
        });
        if (last_page > 5) {
            pages[0].addEventListener("click", () => {
                first_Paging(1);
            })

            pages[pages.length - 1].addEventListener("click", () => {
                last_Paging(Number(pages[pages.length - 1].innerHTML));
            })
            // 添加点击事件到动态分页更新的逻辑
            if (pages.length === 4) {
                pages[2].addEventListener("click", () => {
                    updatePaging(2);
                });
            } else {
                if (Number(pages[1].innerHTML) > 2) {
                    pages[1].addEventListener("click", () => {
                        updatePaging(1);
                    })
                } else if (Number(pages[1].innerHTML) === 2) {
                    pages[1].addEventListener("click", () => {
                        first_Paging(2);
                    })
                }
                if (Number(pages[3].innerHTML) < last_page - 2) {
                    pages[3].addEventListener("click", () => {
                        updatePaging(3);
                    });
                } else if (Number(pages[3].innerHTML) === last_page - 2) {
                    pages[3].addEventListener("click", () => {
                        last_Paging(last_page - 2);
                    })
                }

            }
        }
    }

    function updatePaging(num) {
        const first_page = Number(pages[num].innerText);
        const last_page = pages[pages.length - 1].innerText;

        // 更新分页 HTML
        let paging_box_html = `<div class="page">1</div>`;
        if (first_page > 3) {
            paging_box_html += `<div class="elp">...</div>`
        }
        paging_box_html += `<div class="page">${first_page - 1}</div>
                           <div class="page current">${first_page}</div>`
        if (first_page !== Number(last_page) - 1) {
            paging_box_html += `<div class="page">${first_page + 1}</div>`;
        }
        // paging_box_html += `<div class="page">${first_page + 1}</div>`;
        if (first_page < Number(last_page) - 1) {
            paging_box_html += `<div class="elp">...</div>`
        }
        paging_box_html += `<div class="page">${last_page}</div>`;

        paging_box.innerHTML = paging_box_html;

        // 重新查询新的分页按钮
        pages = document.querySelectorAll(".paging_box .page");

        // 重新绑定事件
        bindEvents();
    }

    function first_Paging(num) {
        const last_page = pages[pages.length - 1].innerText;

        // 更新分页 HTML
        let paging_box_html = ""
        for (let i = 1; i < 4; i++) {
            if (i === num) {
                paging_box_html += `<div class="page current">${i}</div>`
            } else {
                paging_box_html += `<div class="page">${i}</div>`
            }
        }
        paging_box_html += `<div class="elp">...</div>`;
        paging_box_html += `<div class="page">${last_page}</div>`;

        paging_box.innerHTML = paging_box_html;

        // 重新查询新的分页按钮
        pages = document.querySelectorAll(".paging_box .page");

        // 重新绑定事件
        bindEvents();
    }

    function last_Paging(num) {
        console.log("last_Paging", num)
        // 更新分页 HTML
        let paging_box_html = ""
        paging_box_html += `<div class="page">1</div>`;
        paging_box_html += `<div class="elp">...</div>`;
        for (let i = last_page - 3; i < last_page + 1; i++) {
            console.log(i)
            if (i === num) {
                paging_box_html += `<div class="page current">${i}</div>`
            } else {
                paging_box_html += `<div class="page">${i}</div>`
            }
        }

        paging_box.innerHTML = paging_box_html;

        // 重新查询新的分页按钮
        pages = document.querySelectorAll(".paging_box .page");

        // 重新绑定事件
        bindEvents();
    }
}

function load_new_creator(num) {
    $.ajax({
        url: 'http://127.0.0.1:5000/load_new_creators',
        type: 'POST',
        dataType: 'json',
        data: {
            load_count: num
        },
        success: function (response) {
            // 请求成功时执行的函数
            console.log(response.message, response.data)
            const creators_list = document.querySelector(".creators-list >ul")
            creators_list.innerHTML = ""
            if (!response.data) {
                load_flag = false
                creators_list.innerHTML += "<p style='color: #FF3578'>すべての制作者はこちらで以上となります。</p>"
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

                let gender = ""
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
