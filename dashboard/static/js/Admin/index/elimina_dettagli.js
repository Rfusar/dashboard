gestione___modificaANDdettagli(".modifica", "modifica")
gestione___modificaANDdettagli(".piu_dettagli", "utente")
gestione___modificaANDdettagli(".elimina", "utente")

gestione___modificaANDdettagli("#azienda", "#Ragionesociale")
gestione___modificaANDdettagli("#modificaUtente", "#ruolo")






function gestione___modificaANDdettagli(classe, pathFisso) {
    window.addEventListener('click', () => {
        //*CLASSE
        if (classe[0] == ".") {
            if (classe[1] == "e") {
                document.querySelectorAll(classe).forEach((e, i) => {
                    e.addEventListener('click', () => {
                        const R = window.confirm("sei sicuro di eliminare l'utente?")
                        if (R) {
                            fetch("/modificaDB", {
                                method: 'POST',
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    "email": document.querySelectorAll('.email_utente')[i].textContent,
                                    "elimina": true
                                })
                            }).then(res => res.json()).then(d => { document.querySelector('#risposta').textContent = `${d}... aggiorna la pagina` })
                        }
                    })
                })
            }
            else {
                document.querySelectorAll(classe).forEach((e, i) => {
                    e.addEventListener('click', () => { e.setAttribute("href", `/${pathFisso}/${document.querySelectorAll('.email_utente')[i].getAttribute("value")}`) })

                })
            }
        }
        //*ID
        else if (classe[0] == "#") {
            document.querySelector(classe).addEventListener('click', () => {
                if (classe[1] == "a") {
                    document.querySelector(classe).setAttribute('href', `/${document.querySelector(pathFisso).getAttribute('value')}/dettaglio`)
                }
                else if (classe[1] == "m") {
                    document.querySelector(classe).setAttribute('href', `/modifica/${document.querySelector(pathFisso).getAttribute('value')}`)

                }
            })

        }

    })
}