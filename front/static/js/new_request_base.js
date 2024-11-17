console.log("new_request.js")

// 画像追加かつ表示
const fileInput = document.querySelector('[type="file"]');  // ファイル入力要素を取得
const preview_area = document.querySelector(".preview_area");  // 画像プレビューエリアを取得

let preview_area_temp
let imagesArray; // 画像データを保存するための配列

if (preview_area) {
    preview_area_temp = preview_area.innerHTML;  // プレビューエリアの初期状態を保存
    imagesArray = getImagesArray()
    updatePreview();
}

function getImagesArray() {
    const storedImages = localStorage.getItem("imagesArray");
    if (storedImages) {
        try {
            return JSON.parse(storedImages);
        } catch (e) {
            console.error("Error parsing imagesArray from localStorage", e);
            return [];
        }
    }
    return [];
}

// ファイルが選択された時のイベントリスナー
if (fileInput) {
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];  // 最初に選択されたファイルを取得
        if (file) {
            if (validateImages(file)) return//画像の形式とサイズが違う場合
            const reader = new FileReader();  // FileReaderを使用してファイルを読み込む
            reader.onload = function (e) {
                imagesArray.push(e.target.result);  // 画像データを配列に追加
                updatePreview();  // プレビューを更新
            };
            reader.readAsDataURL(file);  // ファイルをData URLとして読み込む
        }
    });
}


// プレビューエリアを更新する関数
function updatePreview() {
    preview_area.innerHTML = preview_area_temp;  // プレビューエリアを初期状態に戻す
    for (let index = imagesArray.length - 1; index >= 0; index--) {
        const imageData = imagesArray[index];
        preview_area.insertAdjacentHTML('afterbegin',
            `<div class="preview" style="background-image:url(${imageData})">
            <button class="close_btn" onclick="deleteImage(${index})">✖</button>
        </div>`
        );
    }
}

// 画像を削除する関数
function deleteImage(index) {
    imagesArray.splice(index, 1);  // 指定されたインデックスの画像を配列から削除
    updatePreview();  // 削除後、プレビューエリアを更新
}

//画像の形式とサイズをチェックする
function validateImages(image) {
    preview_area.lastElementChild.innerHTML = ""
    const maxSize = 2 * 1024 * 1024;  // 最大2MB
    const allowedFormats = ['image/jpeg', 'image/png', 'image/jpg'];  // 許可される画像形式
    let count = 0
    // 画像形式をチェック
    if (!allowedFormats.includes(image.type)) {
        console.log(image.type)
        preview_area.lastElementChild.innerHTML += "サポートされていない画像形式です。JPEG、PNG、jpg形式のみ使用可能です。<br>"
        count++
    }
    // 画像サイズをチェック
    if (image.size > maxSize) {
        preview_area.lastElementChild.innerHTML += "画像サイズが2MBの制限を超えています。"
        count++
    }
    return count !== 0
}

function calendar() {
    // 現在の年と月を使用
    const today = new Date();
    let year = localStorage.getItem("year") ? Number(localStorage.getItem("year")) : today.getFullYear();
    let month = localStorage.getItem("moon") ? Number(localStorage.getItem("moon")) : today.getMonth(); // 当前月份，从0开始
    const year_box = document.querySelector(".step_4 .year")
    const moon_box = document.querySelector(".step_4 .moon")
    const calendar = document.querySelector("table>tbody")
    let text = ""
    let temp_calendar = calendar.innerHTML;
    let temp_moon = Number(localStorage.getItem("moon"));
    let temp_year = Number(localStorage.getItem("year"));

// 初始显示年和月
    if (year_box) year_box.innerText = year;
    if (moon_box) moon_box.innerText = month + 1;

// 渲染日历函数
    function renderCalendar(year, month, isDeadlineDay) {
        console.log(year, month, isDeadlineDay)
        let daysWithSurroundingWeeks;
        if (month === today.getMonth() && year === today.getFullYear()) {
            daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, today, false);
        } else if ((year === today.getFullYear() && month >= today.getMonth()) || year > today.getFullYear()) {
            daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, true);
        } else {
            daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, false);
        }
        update_calendar(daysWithSurroundingWeeks, isDeadlineDay);
    }

    console.log(month, temp_moon, year, temp_year)
// 初始化日历
    renderCalendar(year, month, month === temp_moon && year === temp_year);


// 指定された年、月のカレンダーに前後の週を含めた日付リストを生成する関数
    function getDaysOfMonthWithSurroundingWeeks(year, month, today, next_moon) {
        const daysOfMonth = [];
        const date = new Date(year, month, 1);

        // 前月の最後の週を取得
        const previousMonth = new Date(year, month, 0);  // 前月の最終日
        const lastDayOfPrevMonth = previousMonth.getDate();
        const lastWeekStart = lastDayOfPrevMonth - previousMonth.getDay();  // 前月の最後の日曜日

        // 前月が完全な週でない場合
        if (previousMonth.getDay() !== 6) {
            for (let day = lastWeekStart; day <= lastDayOfPrevMonth; day++) {
                const dayDate = new Date(year, month - 1, day);
                daysOfMonth.push({
                    year: dayDate.getFullYear(),
                    date: dayDate.getDate(),
                    month: dayDate.getMonth() + 1,
                    weekDay: dayDate.getDay(),
                    this_month: false// 現在の月でないことを示す
                });
            }
        }

        // 現在の月のすべての日を追加
        while (date.getMonth() === month) {
            // 次の月の場合
            if (next_moon) {
                daysOfMonth.push({
                    year: date.getFullYear(),
                    date: date.getDate(),
                    month: date.getMonth() + 1,
                    weekDay: date.getDay(),
                    this_month: true,
                    apply: true　// 応募可能んの表示
                });
            } else {
                // 本日から1週間後の日から応募可能
                if (today && date.getDate() > today.getDate() + 7) {
                    daysOfMonth.push({
                        year: date.getFullYear(),
                        date: date.getDate(),
                        month: date.getMonth() + 1,
                        weekDay: date.getDay(),
                        this_month: true,
                        apply: true
                    });
                } else {
                    daysOfMonth.push({
                        year: date.getFullYear(),
                        date: date.getDate(),
                        month: date.getMonth() + 1,
                        weekDay: date.getDay(),
                        this_month: true
                    });
                }
            }
            date.setDate(date.getDate() + 1);  // 次の日に移動
        }

        // 翌月の最初の週を取得
        const nextMonth = new Date(year, month + 1, 1); // 翌月の1日
        // 完全な週でない場合
        if (nextMonth.getDay() !== 0) {
            const daysToAdd = 6 - nextMonth.getDay(); // 最初の日曜日から土曜日までの日数
            for (let day = 1; day <= daysToAdd + 1; day++) {
                const dayDate = new Date(year, month + 1, day);
                daysOfMonth.push({
                    year: dayDate.getFullYear(),
                    date: dayDate.getDate(),
                    month: dayDate.getMonth() + 1,
                    weekDay: dayDate.getDay(),
                    this_month: false // 現在の月でないことを示す
                });
            }
        }
        return daysOfMonth;
    }


// カレンダーを更新する関数
    function update_calendar(daysWithSurroundingWeeks, is_deadline_day) {
        text = ""
        let temp_selected = localStorage.getItem("temp_selected")
        if (temp_selected !== "" && is_deadline_day) {
            calendar.innerHTML = temp_selected
        } else {
            calendar.innerHTML = temp_calendar
            daysWithSurroundingWeeks.forEach((day, i) => {
                if (i % 7 === 0) {
                    text = text + "<tr>"
                }
                if (day.this_month === false) {
                    text = text + `<td class="not_this_moon" data-date="${day.date}"><p>${day.date}</p></td>`
                } else if (day.date === today.getDate() && day.month === today.getMonth() + 1 && day.year === today.getFullYear()) {
                    text = text + `<td data-date="${day.date}"><p class="today">${day.date}</p><p>今日</p></td>`
                } else if (day.apply) {
                    text = text + `<td class="apply" data-date="${day.date}"><p>${day.date}</p><p></p></td>`
                } else {
                    text = text + `<td data-date="${day.date}"><p>${day.date}</p></td>`
                }

                if (i % 7 === 6) {
                    text = text + "</tr>"
                }
            });
        }
        calendar.innerHTML += text;
        addApplyEventListeners()
    }

    function addApplyEventListeners() {
        const apply_list = document.querySelectorAll("table .apply")
        const desired_date = document.querySelector(".desired_date")

        if (apply_list) {
            apply_list.forEach(apply => {
                const date = apply.dataset.date
                apply.addEventListener("click", () => {
                    apply_list.forEach(apply => {
                        apply.classList.remove("selected")
                        apply.lastElementChild.innerHTML = ""
                    })
                    apply.classList.add("selected")
                    apply.lastElementChild.innerHTML = "納期"
                    localStorage.setItem("temp_selected", calendar.innerHTML)
                    localStorage.setItem("moon", month)
                    localStorage.setItem("year", year)
                    temp_moon = month
                    temp_year = year
                    desired_date.innerHTML = `${year}年${month + 1}月${apply.firstElementChild.innerHTML}日まで`
                    document.querySelector('[name="year"]').value = year
                    document.querySelector('[name="moon"]').value = month + 1
                    document.querySelector('[name="day"]').value = apply.firstElementChild.innerHTML
                })
            })
        }
    }

    function switchMonth(direction) {
        if (direction === "prev") {
            month = month > 0 ? month - 1 : 11;
            year = month === 11 ? year - 1 : year;
        } else if (direction === "next") {
            month = month < 11 ? month + 1 : 0;
            year = month === 0 ? year + 1 : year;
        }
        moon_box.innerText = month + 1;
        year_box.innerText = year;
        console.log(month, temp_moon, year, temp_year)
        renderCalendar(year, month, month === temp_moon && year === temp_year);
    }

    const prev = document.querySelector(".header .prev")
    const next = document.querySelector(".header .next")

    if (prev && next) {
        // 前の月ボタンのイベント
        if (prev) prev.addEventListener("click", () => switchMonth("prev"));
        if (next) next.addEventListener("click", () => switchMonth("next"));

    }
}


const options = document.querySelectorAll(".option_areas [type='radio']")
const amount = document.querySelector('[name="amount"]')
if (options) {
    options.forEach(e => {
        e.addEventListener("change", () => {
            const num = Number(e.getAttribute("name").split("_")[1]);
            if (num === 6 && e.value === "2") {
                amount.classList.remove("dis_input_text")
                amount.disabled = false;
            } else if (num === 6) {
                amount.classList.add("dis_input_text")
                amount.disabled = true;
                amount.value = ""
            }
        })
    })
}


const prev_step_btn = document.querySelector(".prev_step_btn")
const next_step_btn = document.querySelector(".next_step_btn")
const progress_bar = document.querySelector(".progress_bar > div")
const kapibara = document.querySelector(".kapibara > div")
const star_boxes = document.querySelectorAll(".star_box")
let progress_value_list = JSON.parse(localStorage.getItem("progress_value_list"));

// let new_request_list = JSON.parse(localStorage.getItem("new_request_list"));

function reset_progress() {
    for (let i = 0; i < progress_value_list.star_boxes_index + 1; i++) {
        if (star_boxes[i]) {
            star_boxes[i].style.filter = "grayscale(0%)"
        }
    }
    progress_bar.style.width = `${progress_value_list.bar_width}%`
    kapibara.style.transform = `translateX(${progress_value_list.kapibara_move}%)`
}

reset_progress()


if (next_step_btn) {
    next_step_btn.addEventListener("click", () => {
        console.log("next_step_btn click")
        progress_value_list.bar_width = progress_value_list.bar_width + 20
        progress_value_list.kapibara_move = progress_value_list.kapibara_move + 100
        progress_value_list.star_boxes_index++
        if (preview_area) {
            localStorage.setItem("imagesArray", JSON.stringify(imagesArray))
        }
        localStorage.setItem("progress_value_list", JSON.stringify(progress_value_list))
        let num = Number(document.querySelector("section>section").getAttribute("class").split("_")[1])
        document.querySelector("section>section form").action = "/new_request_base/0" + String(num + 1)
        document.querySelector("section>section form").submit();
    })
}


if (prev_step_btn) {
    prev_step_btn.addEventListener("click", () => {
        console.log("prev_step_btn click")
        progress_value_list.bar_width = progress_value_list.bar_width - 20
        progress_value_list.kapibara_move = progress_value_list.kapibara_move - 100
        progress_value_list.star_boxes_index--
        if (preview_area) {
            localStorage.setItem("imagesArray", JSON.stringify(imagesArray))
        }
        localStorage.setItem("progress_value_list", JSON.stringify(progress_value_list))
        let num = Number(document.querySelector("section>section").getAttribute("class").split("_")[1])
        document.querySelector("section>section form").action = "/new_request_base/0" + String(num - 1)
        document.querySelector("section>section form").submit();
    })
}


check_box()

const step_4 = document.querySelector(".step_4")
if (step_4) {
    calendar()
}


const step_5 = document.querySelector(".step_5")
if (step_5) {
    final_confirmation()
    add_new_request()
}

function final_confirmation() {
    const final_confirmation_image = document.querySelector(".final_confirmation_image")
    const images = getImagesArray()
    final_confirmation_image.innerHTML = ""
    for (let index = images.length - 1; index >= 0; index--) {
        const imageData = images[index];
        final_confirmation_image.innerHTML += `<div class="img" style="background-image:url(${imageData})"></div>`
    }
}

function add_new_request() {
    const submit_btn = document.querySelector(".submit_btn")
    const images = getImagesArray()
    submit_btn.addEventListener("click", () => {
        $.ajax({
            url: 'http://127.0.0.1:5000//add_new_request',
            type: 'POST',
            contentType: 'application/json',  // 送信するデータの種類をJSONに設定
            dataType: 'json',
            data: JSON.stringify({images: images}),  // オブジェクト全体をJSON文字列に変換
            success: function (response) {
                // 请求成功时执行的函数
                alert(response.message)
                localStorage.clear();
                document.querySelector(".add_suc").submit();
            },
            error: function (xhr, status, error) {
                // 请求失败时执行的函数
                console.error('Error message:', error);
            }
        });
    })
}