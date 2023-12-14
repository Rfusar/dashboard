const email = document.querySelector('#exampleInputEmail')
const password = document.querySelector('#exampleInputPassword')
const btn = document.querySelector('#btnLogin')

let EMAIL;
let PASSWORD;
let ragioneSociale;

email.addEventListener('change', () => {
    EMAIL = checkValidation(email.value)
    if (typeof EMAIL === 'string' && typeof PASSWORD === "string") {
        btn.classList.remove('disabled')
        btn.setAttribute('aria-disabled', 'false')
    }
})
password.addEventListener('change', () => {
    PASSWORD = ValidationPassword(password.value)
    if (typeof EMAIL === 'string' && typeof PASSWORD === "string") {
        btn.classList.remove('disabled')
        btn.setAttribute('aria-disabled', 'false')
    }
})




//funzionalita in piu
document.addEventListener("keydown", (e)=>{

    if ((e.ctrlKey || e.metaKey) && e.key === "5") {

        console.log(EMAIL)
        console.log(PASSWORD)
        console.log(ragioneSociale)


    }
})