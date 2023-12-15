const fieldDEL = document.querySelectorAll(".DELETE")
const fieldMOD = document.querySelectorAll(".MODIFY")
const campi = [fieldDEL, fieldMOD]

identificativo(campi)
let ID_per_disattivazione = ""
prova_perSemplificare(inputRadio, check)

//func per semplificare le chiamate ad --const campi
function prova_perSemplificare(func1, func2) {
    for (const campo of campi) {
        // function inputRadio, function check
        if (func1 && func2) {
            func1(campo)
            func2(campo)
        }
        //function campi__TOTALI
        else if (func1) {
            const TOTCampi = []
            func1(campo, TOTCampi)
            return TOTCampi
        }
    }
}

//*FUNCS RADIO
//attiva/disattiva
function check(elementi) {
    elementi.forEach(e => {
        e.addEventListener('click', () => {
            if (ID_per_disattivazione == e.getAttribute("id")) {
                e.checked == true ? e.checked = false : e.checked = true
                if (e.getAttribute("secondoCheck") == "false") {
                    e.checked = true
                    e.setAttribute("secondoCheck", "true0")
                }
                else if (e.getAttribute("secondoCheck") == "true0") {
                    e.checked = false
                    e.setAttribute("secondoCheck", "false")
                }
                e.getAttribute("secondoCheck") == "true" ? e.setAttribute("secondoCheck", "false") : null
                ID_per_disattivazione = ""
            }
            ID_per_disattivazione = e.getAttribute("id")
        })
    })
}
function identificativo(arrays) {
    elementi = []
    for (const array of arrays) {
        for (const e of array) { elementi.push(e) }
    }
    let count = 0
    for (const e of elementi) {
        let ID = "radio" + count
        e.setAttribute("id", ID)
        count++
    }
}
//cosi posso utilizzare gli input radio correttamente
function inputRadio(elementi) {
    let count = 0
    elementi.forEach(e => { e.setAttribute("name", String(count)); count++ })
}
function campi__TOTALI(campo, TOTCampi) { campo.forEach(e => { TOTCampi.push(e) }) }