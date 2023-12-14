fetch("/tableInfo").then(res => res.json()).then(d => {
    const regex1 = /[a-zA-Z" "]/g;
    const IMP_IPOTECA_array = []
    //zoom tabella
    const DATI = {}
    const documenti_mutuo = []
    for (let i = 0; i < d["documenti_mutuo"].length; i++) {

        let importo = d["documenti_mutuo"][i][5]
        let impIpoteca = d["documenti_mutuo"][i][8]

        let lettere_importo = importo.match(regex1);
        let lettere_impIpoteca = impIpoteca.match(regex1);

        let IMPORTO = checkDECIMALI(checkNUMERI(importo, lettere_importo))
        let IMP_IPOTECA = checkDECIMALI(checkNUMERI(impIpoteca, lettere_impIpoteca))

        IMP_IPOTECA_array.push(checkNUMERI(impIpoteca, lettere_impIpoteca))
        let ogg = {
            "♦ Tipo di contratto: ": d["documenti_mutuo"][i][0],
            "♦ Istituto di credito mutuante: ": d["documenti_mutuo"][i][1],
            "♦ Mutuatari/o: ": d["documenti_mutuo"][i][2],
            "♦ Codice fiscale mutuatario: ": d["documenti_mutuo"][i][3],
            "♦ Data erogazione: ": d["documenti_mutuo"][i][4],
            "♦ Importo: ": IMPORTO,
            "♦ Durata: ": d["documenti_mutuo"][i][6],
            "♦ Tasso fisso/variabile: ": d["documenti_mutuo"][i][7],
            "♦ Importo iscrizione ipoteca volontaria: ": IMP_IPOTECA,
            "♦ Grado ipoteca: ": d["documenti_mutuo"][i][9],
            "♦ Importo fideiussione: ": d["documenti_mutuo"][i][10],
            "♦ Fideiussore/i: ": d["documenti_mutuo"][i][11],
            "♦ N beni ipotecati: ": d["documenti_mutuo"][i][12],
            "♦ Indirizzo beni ipotecati: ": d["documenti_mutuo"][i][13],
            "♦ Categoria catastale: ": d["documenti_mutuo"][i][14],
            "♦ Foglio: ": d["documenti_mutuo"][i][15],
            "♦ Particella: ": d["documenti_mutuo"][i][16],
            "♦ Mappale: ": d["documenti_mutuo"][i][17]
        }
        documenti_mutuo.push(ogg)
    }
    DATI['documenti mutuo'] = documenti_mutuo

    const PARAGRAFI_MUTUO = []
    for (let i = 0; i < DATI['documenti mutuo'].length; i++) {
        let a = new Tabella(DATI['documenti mutuo'][i]).creazione_info_MUTUI()
        PARAGRAFI_MUTUO.push(a)
    }

    // GESTIONE CHIUSURA/APERTURA PAGINA
    let div_piuDettagli = document.querySelector("#_piuDettagli");
    let btn_piuDettagli = document.querySelectorAll(".piuDettagli");
    let doc = document.querySelectorAll(".IDDocumento");

    let c = undefined; let apertura = undefined; let count = 0
    btn_piuDettagli.forEach((btn, index) => {
        btn.addEventListener("click", () => {
            let b = btn;
            if (c == b) {
                div_piuDettagli.style.height = "0px";
                div_piuDettagli.style.width = "0px";
                setTimeout(() => {
                    div_piuDettagli.innerHTML = ""
                }, 800)
                apertura = 1
            }
            else {
                div_piuDettagli.style.height = "max-content";
                div_piuDettagli.style.width = "1350px";
                if (count > 0) { div_piuDettagli.innerHTML = "" }
                for (let i = 0; i < PARAGRAFI_MUTUO.length; i++) {
                    if (PARAGRAFI_MUTUO[i][0].textContent.includes(doc[index].textContent)) {
                        for (let j = 0; j < PARAGRAFI_MUTUO[i].length; j++) {
                            div_piuDettagli.append(PARAGRAFI_MUTUO[i][j])
                        }
                    }
                }
                count++
            }
            if (apertura == 1) { c = undefined; apertura = undefined; count = 0 }
            else { c = b }
        });
    });

    //sistemazione nella tabella
    document.querySelectorAll(".Ipoteca").forEach((e) => {
        let lettere_e = e.textContent.match(regex1);
        for (let imp of IMP_IPOTECA_array) {
            if (checkNUMERI(e.textContent, lettere_e) == imp) {
                e.textContent = checkDECIMALI(imp)
                break
            }
        }
    })
    document.querySelectorAll(".data").forEach((e) => {
        const dati = e.textContent.split(" ")
        let giorno = dati[0]
        let mese = setMESE(dati)
        let anno = dati[2]
        e.textContent = `${giorno}/${mese}/${anno}`
    })
})


function checkNUMERI(importo, lettere_importo) {
    if (lettere_importo != null) {
        lettere_importo = lettere_importo.join("")
        let Importo = importo.substring(lettere_importo.length)

        let IMPORTO_x = Importo; return IMPORTO_x

    } else { let IMPORTO_x = importo; return IMPORTO_x }
}
function setMESE(dati) {
    switch (dati[1].toLowerCase()) {
        case "gennaio":
            return "01"
        case "febbraio":
            return "02"
        case "marzo":
            return "03"
        case "aprile":
            return "04"
        case "maggio":
            return "05"
        case "giugno":
            return "06"
        case "luglio":
            return "07"
        case "agosto":
            return "08"
        case "settembre":
            return "09"
        case "ottobre":
            return "10"
        case "novembre":
            return "11"
        case "dicembre":
            return "12"
    }
}
function checkDECIMALI(imp) {
    function checkFinale(decimale, parte_intera) {
        let FASE1 = ""
        for (let cifra of parte_intera) {
            decimale % 3 == 0 && decimale != 0 ? FASE1 += `.${cifra}` : FASE1 += cifra
            decimale++
        }
        let FASE2 = ""
        for (let cifra = FASE1.length-1; cifra >= 0; cifra--) { 
            FASE2 += FASE1[cifra] 
            cifra == 0 ? FASE2 += ",00" : null
        }
        return FASE2
    }
    let a = ""
    for (let cifra of imp) {
        cifra == "," || cifra == "." ? cifra = "," : null
        a += cifra
    }
    //REVERSE
    let b = ""
    for (let cifra = a.length - 1; cifra >= 0; cifra--) { b += a[cifra] }
    
    //LAVORAZIONE FINALE
    let CIFRA = ""
    let decimale = 0
    if (b[2] == ",") {
        let parte_intera = b.split(",")[1]
        CIFRA = checkFinale(decimale, parte_intera)
    }
    else {
        let parte_intera = b
        CIFRA = checkFinale(decimale, parte_intera)
    }

    return CIFRA
}


