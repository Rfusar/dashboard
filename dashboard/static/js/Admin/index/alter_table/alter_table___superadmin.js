document.querySelector("#btn").addEventListener("click", () => {
    const fieldDEL = document.querySelectorAll(".DELETE")
    const fieldMOD = document.querySelectorAll(".MODIFY")
    const aziende = document.querySelectorAll(".azienda_utente")
    const nomi = document.querySelectorAll(".nome_utente")
    const cognomi = document.querySelectorAll(".cognome_utente")
    const emails = document.querySelectorAll(".email_utente")

    const utenti = []
    for (let i = 0; i < nomi.length; i++) {
        const utente = {}

        utente['azienda'] = aziende[i].textContent
        utente['nome'] = nomi[i].textContent
        utente['cognome'] = cognomi[i].textContent
        utente['email'] = emails[i].textContent
        utente['elimina'] = fieldDEL[i].checked
        utente['modifica'] = fieldMOD[i].checked

        if (utente['elimina'] || utente['modifica']) { utenti.push(utente) }
    }

    //js/Admin/index/invio_a_server.js
    manda_a_SERVER("/modificaDB", utenti)
})