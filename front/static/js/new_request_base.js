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

function getDaysOfMonthWithSurroundingWeeks(year, month) {
    const daysOfMonth = [];
    const date = new Date(year, month, 1);

    // 前一个月的最后一周
    const previousMonth = new Date(year, month, 0); // 上个月的最后一天
    const lastDayOfPrevMonth = previousMonth.getDate();
    const lastWeekStart = lastDayOfPrevMonth - previousMonth.getDay(); // 上个月的最后一个星期天

    if (previousMonth.getDay() !== 6) {
        for (let day = lastWeekStart; day <= lastDayOfPrevMonth; day++) {
            const dayDate = new Date(year, month - 1, day);
            daysOfMonth.push({
                date: dayDate.getDate(),
                month: dayDate.getMonth() + 1,
                weekDay: dayDate.getDay()
            });
        }
    }

    // 当前月份的所有天
    while (date.getMonth() === month) {
        daysOfMonth.push({
            date: date.getDate(),
            month: date.getMonth() + 1,
            weekDay: date.getDay()
        });
        date.setDate(date.getDate() + 1); // 移动到下一个日期
    }

    // 下一个月的第一周
    const nextMonth = new Date(year, month + 1, 1); // 下个月的第一天
    if (nextMonth.getDay() !== 0) {
        const daysToAdd = 6 - nextMonth.getDay(); // 从第一个星期天开始到第一个周六
        for (let day = 1; day <= daysToAdd + 1; day++) {
            const dayDate = new Date(year, month + 1, day);
            daysOfMonth.push({
                date: dayDate.getDate(),
                month: dayDate.getMonth() + 1,
                weekDay: dayDate.getDay()
            });
        }
    }
    return daysOfMonth;
}

// 使用当前年份和月份
const today = new Date();
const year = today.getFullYear();
const month = today.getMonth(); // 当前月份，从0开始
const year_box = document.querySelector(".step_4 .year")
const moon_box = document.querySelector(".step_4 .moon")
year_box.innerText = year
moon_box.innerText = month + 1


const daysWithSurroundingWeeks = getDaysOfMonthWithSurroundingWeeks(year, month);
const calendar = document.querySelector("table>tbody")
let test = ""

daysWithSurroundingWeeks.forEach((day, i) => {
    console.log(`日期: ${day.month}月${day.date}日, 星期: ${['日', '一', '二', '三', '四', '五', '六'][day.weekDay]}`);
    if (i % 7 === 0) {
        test = test + "<tr>"
    }
    if (day.date === today.getDate()) {
        test = test + `<td><p class="today">${day.date}</p><p>今日</p></td>`
    } else {
        test = test + `<td><p>${day.date}</p></td>`
    }
    if (i % 7 === 6) {
        test = test + "</tr>"
    }
});
console.log(test)
calendar.insertAdjacentHTML("beforeend", test);