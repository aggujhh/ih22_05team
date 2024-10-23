console.log(registration.js)


const user_types = document.querySelectorAll('[name="user_type"]')
const myForm = document.querySelector('#myForm')
const user_type_data = document.querySelector('[name="user_type_data"]')

user_types.forEach(user_type => {
    console.log(user_type.value)
    user_type.addEventListener("change", () => {
        user_type_data.value = user_type.value
        myForm.submit();
    })
})

