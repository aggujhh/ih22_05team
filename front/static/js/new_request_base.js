console.log("new_request.js")

// 画像追加かつ表示
const fileInput = document.querySelector('[type="file"]');  // ファイル入力要素を取得
const preview_area = document.querySelector(".preview_area");  // 画像プレビューエリアを取得
// const creator_image = document.querySelector('[name="creator_image"]')
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
                updatePreview();  // プレビューを更新
            };
            reader.readAsDataURL(file);  // ファイルをData URLとして読み込む
        }
    });
}


// プレビューエリアを更新する関数
function updatePreview() {
    preview_area.innerHTML = preview_area_temp;  // プレビューエリアを初期状態に戻す
    // if (imagesArray.length === 0) {
    //     creator_image.value = ""
    // } else {
    //     creator_image.value = "have_img"
    // }
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
    console.log(111)
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

// if (creator_btn) {
//     creator_btn.addEventListener(("click"), () => {
//         console.log(!not_full())
//         if (checkBox.checked && !not_full()) {
//             console.log("OK")
//             $.ajax({
//                 url: 'http://127.0.0.1:5000/upload_img',
//                 type: 'POST',
//                 contentType: 'application/json',  // 送信するデータの種類をJSONに設定
//                 dataType: 'json',
//                 data: JSON.stringify({images: imagesArray}),  // オブジェクト全体をJSON文字列に変換
//                 success: function (response) {
//                     // 请求成功时执行的函数
//                     console.log('Reset successful');
//                     console.log(response.urls)
//                     creator_image.value = JSON.stringify(response.urls);
//                     document.querySelector("#creator_form").submit();
//                 },
//                 error: function (xhr, status, error) {
//                     // 请求失败时执行的函数
//                     console.error('Error response:', error.response);
//                     console.error('Error message:', error.message);
//                 }
//             });
//             // document.querySelector("#requester_form").submit();
//         } else {
//             if (!checkBox.checked) {
//                 checkBox.parentNode.parentNode.querySelector(".error_msg").innerText = `利用規約をよくお読みの上、確認ボタンをクリックしてください。`
//             }
//             creator_btn.classList.add("dis_btn")
//         }
//     })
// }


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
                    date: date.getDate(),
                    month: date.getMonth() + 1,
                    weekDay: date.getDay(),
                    this_month: true,
                    apply: true
                });
            } else {
                daysOfMonth.push({
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
                date: dayDate.getDate(),
                month: dayDate.getMonth() + 1,
                weekDay: dayDate.getDay(),
                this_month: false // 現在の月でないことを示す
            });
        }
    }
    return daysOfMonth;
}

// 現在の年と月を使用
const today = new Date();
let year = today.getFullYear();
let month = today.getMonth(); // 当前月份，从0开始
const year_box = document.querySelector(".step_4 .year")
const moon_box = document.querySelector(".step_4 .moon")
year_box.innerText = year
moon_box.innerText = month + 1

// 前後の週を含むカレンダー日付を取得
const daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, today, false);
const calendar = document.querySelector("table>tbody")
let text = ""
const temp_calendar = calendar.innerHTML
let temp_selected = ""
let temp_moon = ""
let temp_year = ""

// カレンダーを更新する関数
function update_calendar(daysWithSurroundingWeeks, is_today) {
    text = ""
    if (temp_selected !== "" && is_today) {
        calendar.innerHTML = temp_selected
    } else {
        calendar.innerHTML = temp_calendar
        daysWithSurroundingWeeks.forEach((day, i) => {
            if (i % 7 === 0) {
                text = text + "<tr>"
            }
            if (day.this_month === false) {
                text = text + `<td class="not_this_moon" data-date="${day.date}"><p>${day.date}</p></td>`
            } else if (day.date === today.getDate() && day.month === today.getMonth() + 1) {
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
                temp_selected = calendar.innerHTML
                temp_moon = document.querySelector(".moon").innerHTML
                temp_year = Number(document.querySelector(".year").innerHTML)
                desired_date.innerHTML = `${temp_year}年${temp_moon}月${apply.firstElementChild.innerHTML}日まで`
            })
        })
    }
}

update_calendar(daysWithSurroundingWeeks, true)

const prev = document.querySelector(".header .prev")
const next = document.querySelector(".header .next")

// 前の月ボタンのイベント
prev.addEventListener("click", () => {
    if (month > 0) {
        month--
    } else {
        month = 11
        year--
    }
    moon_box.innerText = month + 1
    year_box.innerText = year
    let daysWithSurroundingWeeks
    if (month === today.getMonth() && year === today.getFullYear()) {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, today, false)
    } else if (month >= today.getMonth() || year > today.getFullYear()) {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, true)
    } else {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, false)
    }
    console.log("month", month, temp_moon - 1)
    console.log("year", year, temp_year)
    if (month === temp_moon - 1 && year === temp_year) {
        console.log(123)
        update_calendar(daysWithSurroundingWeeks, true)
    } else {
        update_calendar(daysWithSurroundingWeeks, false)
    }
})

// 次の月ボタンのイベント
next.addEventListener("click", () => {
    if (month < 11) {
        month++
    } else {
        month = 0
        year++
    }
    moon_box.innerText = month + 1
    year_box.innerText = year
    let daysWithSurroundingWeeks
    if (month === today.getMonth() && year === today.getFullYear()) {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, today, false)
    } else if (month >= today.getMonth() || year > today.getFullYear()) {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, true)
    } else {
        daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month, null, false)
    }
    if (month === temp_moon - 1 && year === temp_year) {
        console.log(123)
        update_calendar(daysWithSurroundingWeeks, true)
    } else {
        update_calendar(daysWithSurroundingWeeks, false)
    }
})
