fetch("/superadminCheck").then(res => res.json()).then(d => {
    const DATI = {}
    const documenti = []
    for (let i = 0; i < d["aziende"].length; i++) {
        let ogg = {
            "Id": d["aziende"][i][0],
            "Nome": d["aziende"][i][1],
            "Partita IVA": d["aziende"][i][2],
            "Indirizzo": d["aziende"][i][3],
            "Comune": d["aziende"][i][4],
            "Provincia": d["aziende"][i][5],
            "Cap": d["aziende"][i][6],
            "Nazione": d["aziende"][i][7],
            "Email": d["aziende"][i][8],
            "Pec": d["aziende"][i][9],
            "Tel": d["aziende"][i][10],
        }
        documenti.push(ogg)
    }
    DATI['aziende'] = documenti
    const PARAGRAFI_DOCUMENTI = []
    for (let i = 0; i < DATI['aziende'].length; i++) {
        let a = new Tabella(DATI['aziende'][i]).creazione_info_AZIENDE()
        PARAGRAFI_DOCUMENTI.push(a)
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
                div_piuDettagli.style.width = "1050px";
                if (count > 0) { div_piuDettagli.innerHTML = "" }
                for (let i = 0; i < PARAGRAFI_DOCUMENTI.length; i++) {
                    if (PARAGRAFI_DOCUMENTI[i][0].textContent.includes(doc[index].textContent)) {
                        for (let j = 0; j < PARAGRAFI_DOCUMENTI[i].length; j++) {
                            div_piuDettagli.append(PARAGRAFI_DOCUMENTI[i][j])
                        }
                    }
                }
                count++
            }
            if (apertura == 1) { c = undefined; apertura = undefined; count = 0 }
            else { c = b }
        });
    });
})