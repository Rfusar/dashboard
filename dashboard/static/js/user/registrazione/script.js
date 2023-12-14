const nome = document.querySelector('#exampleFirstName')
const cognome = document.querySelector('#exampleLastName')
const RG = document.querySelector('#ragioneSociale')
const email = document.querySelector('#exampleInputEmail')
const password = document.querySelector('#exampleInputPassword')
const Rpassword = document.querySelector('#exampleRepeatPassword')
const btn = document.querySelector('#btn')

let NOME;
let COGNOME;
let EMAIL;
let PASSWORD;
let ragioneSociale;

nome.addEventListener('change', () => {
    for (let i in nome.value) {
        if (nome.value[i] == ' ' || nome.value[i] == '/' || nome.value[i] == '\\' || nome.value[i] == '""' || nome.value[i] == '"'){
            window.alert('ERRORE')
            nome.value = ''
        }
    }
    NOME = nome.value
})

cognome.addEventListener('change', () => {
    for (let i in cognome.value) {
        if (cognome.value[i] == ' ' || cognome.value[i] == '/' || cognome.value[i] == '\\' || cognome.value[i] == '""' || cognome.value[i] == '"') {
            window.alert('ERRORE')
            cognome.value = ''
        }
        COGNOME = cognome.value
    }
})

RG.addEventListener('change', () => {
    for (let i in RG.value) {
        if (RG.value[i] == '/' || RG.value[i] == '\\' || RG.value[i] == '""' || RG.value[i] == '"') {
            window.alert('ERRORE')
            RG.value = ''
        }
        ragioneSociale = RG.value
    }
})

email.addEventListener('change', () => {

    EMAIL = checkValidation(email.value)
})

password.addEventListener('change', () => {
   PASSWORD = ValidationPassword(password.value)
})







btn.addEventListener('mouseover', () => {

    if (password.value == Rpassword.value) {

        const Utente = {

            "nome": NOME,
            "cognome": COGNOME,
            "email": EMAIL,
            "password": PASSWORD,
            "ragioneSociale": ragioneSociale
        }
        
        btn.setAttribute('href', `/fetchRegister/${Utente['nome']}/${Utente['cognome']}/${Utente['email']}/${Utente['password']}/${Utente['ragioneSociale']}`)
        console.log(btn.attributes[0])
        
    }
    else if (password.value != Rpassword.value) {
        const a = () => {
            window.alert('Password diverse')
            password.value = ''
            Rpassword.value = ''
        }
        a()
    }

})



document.addEventListener("keydown", function (event) {

    if ((event.ctrlKey || event.metaKey) && event.key === "5") {

        console.log(NOME)
        console.log(COGNOME)
        console.log(EMAIL)
        console.log(PASSWORD)
        console.log(ragioneSociale)

       

    }
})