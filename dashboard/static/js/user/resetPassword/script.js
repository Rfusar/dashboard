const email = document.querySelector('#exampleInputEmail')
const nuova_password = document.querySelector('#newPass')
const btn = document.querySelector('#btn')

let EMAIL;
let NEWpassword;

email.addEventListener('change', () => {

    EMAIL = checkValidation(email.value)
    if (typeof EMAIL === 'string') {

        btn.classList.remove('disabled')
        btn.setAttribute('aria-disabled', 'false')
    }
})
nuova_password.addEventListener('change', () => {

    NEWpassword = ValidationPassword(nuova_password.value)
    if (typeof NEWpassword === 'string') {

        btn.classList.remove('disabled')
        btn.setAttribute('aria-disabled', 'false')
    }
})

btn.addEventListener('click', () => {

    btn.setAttribute('href', `/fetchResetPassword/${EMAIL}/${NEWpassword}`)
})