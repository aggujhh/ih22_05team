console.log("request.js")


const big_img = document.querySelector(".big_img")
const small_images = document.querySelectorAll(".small_img div");
console.log(small_images)

small_images.forEach((small_img) => {
    small_img.addEventListener("click", (event) => {
        reset_border()
        small_img.style.border = "2px solid #ec7fb1"
        big_img.style.backgroundImage = getComputedStyle(small_img).backgroundImage
    });
})

function reset_border() {
    small_images.forEach((e) => {
        e.style.border = "1.5px solid #818181"
    })
}