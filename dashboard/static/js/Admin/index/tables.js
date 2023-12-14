class Calcoli {
    constructor(nome, token) {
        this.nome = nome,
            this.token = token
    }
    check() {
        let s = 0
        for (const c of this.token) { s += c }
        const ogg = { "azienda": this.token, "token": this }
        return ogg
    }
}

fetch("/dati").then(res => res.json()).then(d => {
    let s = 0
    for (let i of d[0]) { s += i }

    let costo = s * 0.004 * 1 / 1000
    let vendita = s * 0.004 * 1.335 / 1000
    let ricavo = vendita - costo
    document.querySelector('#costo').textContent = `COSTO: €${costo.toFixed(3)}`
    document.querySelector('#vendita').textContent = `VENDITA: €${vendita.toFixed(3)}`
    document.querySelector('#ricavo').textContent = `GUADAGNO: €${ricavo.toFixed(3)}`

    document.querySelector('#tokenTOTALI').textContent = `TOKEN UTILIZZATI: ${s}`
})



