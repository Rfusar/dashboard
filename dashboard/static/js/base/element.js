class AMICI {
    constructor(nome, email) {
        this.nome = nome
        this.email = email
    }
}
class CHAT {
    constructor(chat) {
        this.chat = chat
    }
}
class NOTIFICA {
    constructor(mia, tutti) {
        this.mia = mia
        this.tutti = tutti
    }
}
let User = {}
let Amici = []
let chat_attive = []
let notifiche_attive = []

fetch("/messaggi")
    .then(res => res.json())
    .then(d => {

        User['nome'] = d[0]['utente'][0]
        User['email'] = d[0]['email']

        for (let i in d[1]) {
            for (let j in d[1][i]) {
                let chat = new CHAT(d[1][i][j])
                chat_attive.push(chat)
            }
        }

        for (let i in d[2]) {
            let amicoNOME = d[2][i]['utente'][0]
            let amicoEMAIL = d[2][i]['email']
            let Amico = new AMICI(amicoNOME, amicoEMAIL)
            Amici.push(Amico)
        }

        for (let i in d[3]) {
            let notifica = new NOTIFICA(d[3][i].mia, d[3][i].altri)
            notifiche_attive.push(notifica)
        }

        /*console.log(chat_attive)
        console.log(notifiche_attive)
        console.log(Amici)
        console.log(User)
        console.log('')
        console.log('lavoro di dati')
        console.log(connChat())
        console.log('dati totali')
        console.log(d)*/

    })
    .catch(err => console.log(err))