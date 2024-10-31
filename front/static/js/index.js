console.log("index.js");

const carousel_left_btn = document.querySelector(".carousel_button_left");
const carousel_right_btn = document.querySelector(".carousel_button_right");
const dot = document.querySelectorAll(".dot");
const carousel_imgs = document.querySelector(".carousel_imgs");
const carousel_box = document.querySelector(".carousel");

let index = 0;
let time = 0;


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
    }, 3000)
}

//点击左键
carousel_left_btn.addEventListener("click", () => {
    desc();
})
//点击右键
carousel_right_btn.addEventListener("click", () => {
    add();
    console.log(123)
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