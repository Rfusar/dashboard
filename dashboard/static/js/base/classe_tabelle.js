class Tabella {
    constructor(dati) { this.dati = dati }
    creazione_info_AZIENDE() { 
        const paragrafo = []
        const grassetto = []
        const titoli = [
            "♦ Id: ",
            "♦ Nome: ",
            "♦ Partita IVA: ",
            "♦ Indirizzo: ",
            "♦ Comune: ",
            "♦ Provincia: ",
            "♦ Cap: ",
            "♦ Nazione: ",
            "♦ Email: ",
            "♦ Pec: ",
            "♦ Tel: "
        ]
        const titoli_ = [
            "Id",
            "Nome",
            "Partita IVA",
            "Indirizzo",
            "Comune",
            "Provincia",
            "Cap",
            "Nazione",
            "Email",
            "Pec",
            "Tel"
        ]
        for (let i = 0; i < titoli.length; i++) {
            let p = document.createElement('p'); p.classList = "dati"
            let pS = document.createElement('strong')
            paragrafo.push(p)
            grassetto.push(pS)
        }
        for (let i = 0; i < grassetto.length; i++) { 
            grassetto[i].textContent = titoli[i]
            paragrafo[i].append(grassetto[i]) 
            paragrafo[i].append(this.dati[titoli_[i]]) 
        }
        return paragrafo
    }
}