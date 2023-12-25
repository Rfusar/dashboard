//PAGINA => ListaColleghi
if (document.title == "Lista colleghi") {
    gestione___ELI_MOD_DET(".modifica", null, "modificaUtente")
    gestione___ELI_MOD_DET(".piu_dettagli", null, "dettaglioUtente")
    gestione___ELI_MOD_DET(".elimina", null, "eliminaUtente")
}
//PAGINA => listaAziende
else if (document.title == "Lista aziende") {
    gestione___ELI_MOD_DET(".elimina", null, "eliminaAzienda")
    gestione___ELI_MOD_DET(".modifica", null, "modificaAzienda")
    gestione___ELI_MOD_DET(".piu_dettagli", null, "dettaglioAzienda")
}
//PAGINA => DettaglioUtente
else if (document.title == "Area utente") {
    //btn dettaglio azienda
    gestione___ELI_MOD_DET("#azienda", "#Ragionesociale", "dettaglioAzienda")
    // btn modifica utente
    gestione___ELI_MOD_DET("#modificaUtente", "#ruolo", "modificaUtente")
}


function gestione___ELI_MOD_DET(identificativo, pathFisso, pathFinale) {
    window.addEventListener('click', () => {
        //IDENTIFICATIVO = CLASSE
        if (identificativo[0] == ".") {
            //*PAGINA => ListaColleghi
            if (identificativo[1] == "e" && pathFinale[pathFinale.length - 1] == "e") {
                document.querySelectorAll(identificativo).forEach((e, i) => {
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
            else if (identificativo[1] != "e" && pathFinale[pathFinale.length - 1] == "e") {
                document.querySelectorAll(identificativo).forEach((e, i) => {
                    e.addEventListener('click', () => { e.setAttribute("href", `/${document.querySelectorAll('.email_utente')[i].getAttribute("value")}/${pathFinale}`) })

                })
            }
            //*PAGINA => listaAziende
            else if (identificativo[1] != "e" && pathFinale[pathFinale.length - 1] == "a") {
                let valore = document.querySelectorAll('.Ragionesociale')
                let img = document.querySelectorAll(identificativo)
                img.forEach((_, i) => {
                    img[i].addEventListener('click', () => {
                        img[i].setAttribute('href', `/${valore[i].getAttribute('value')}/${pathFinale}`)
                    })
                })
            }
        }
        //IDENTIFICATIVO = ID
        else if (identificativo[0] == "#") {
            //*PAGINA => DettaglioUtente
            document.querySelector(identificativo).addEventListener('click', () => {
                if (identificativo[1] == "a") {
                    document.querySelector(identificativo)
                        .setAttribute('href', `/${document.querySelector(pathFisso).getAttribute('value')}/${pathFinale}`)
                }
                else if (identificativo[1] == "m") {
                    document.querySelector(identificativo)
                        .setAttribute('href', `/${document.querySelector(pathFisso).getAttribute('value')}/${pathFinale}`)

                }
            })

        }

    })
}
