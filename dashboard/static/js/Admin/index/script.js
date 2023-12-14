const comandi = ["nessuna", "prima lettera", "intera parola"]
    const colore = {
        "colore": [true, {
            
            "utente": [true, "black"],
            "admin": [true, "red"],
            "superuser": [true, "blue"]
        }]
    }
document.querySelectorAll(".ruolo").forEach(e => {
    //MAISUCOLE
    const comando = comandi[1]
    let termine = ""
    if (comando == "nessuna") {
        for (let i = 0; i < e.textContent.length; i++) { termine += e.textContent[i] }
    }

    else if (comando == "prima lettera") {
        const maiuscola = e.textContent[0].toLocaleUpperCase()
        for (let i = 0; i < e.textContent.length; i++) {
            if (i == 0) { termine += maiuscola }
            else { termine += e.textContent[i] }
        }
    }
    else if (comando == "intera parola") {
        for (let i = 0; i < e.textContent.length; i++) { termine += e.textContent[i].toLocaleUpperCase() }
    }
    
    //COLORI
    if (colore['colore'][0]) {
        if (colore['colore'][1]['utente'][0]) {
            if (termine == "utente" || termine == "Utente" || termine == "UTENTE") {
                e.style.color = colore['colore'][1]['utente'][1]
            }
        }
        if (colore['colore'][1]['admin'][0]) {
            if (termine == "admin" || termine == "Admin" || termine == "ADMIN") {
                e.style.color = colore['colore'][1]['admin'][1]
            }
        }
        if (colore['colore'][1]['superuser'][0]) {
            if (termine == "superuser" || termine == "Superuser" || termine == "SUPERUSER") {
                e.style.color = colore['colore'][1]['superuser'][1]
            }
        }
    }
    e.textContent = termine
})


