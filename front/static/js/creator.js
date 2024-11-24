console.log("creator.js")

window.addEventListener("load", () => {
    show_image()
})


function show_image() {
    const produced_images = document.querySelectorAll(".produced_image")
    produced_images.forEach((e) => {
        e.addEventListener("click", () => {
            console.log(e.parentNode)
            e.parentNode.submit()
        })
    })
}
