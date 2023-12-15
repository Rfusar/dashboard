const btnNotifiche = document.querySelector('#btnNotifiche')
const btnMessaggi = document.querySelector('#btnMessaggi')

const Chat = document.querySelector('.Chat')

const btn = document.querySelector('#INVIA')
const displayChat = document.querySelector('#DISPLAY')
const btnExit = document.querySelector('#BTNEXIT')




btnExit.addEventListener('click', () => { Chat.style.display = 'none' })

//NOTIFICHE
btnNotifiche.addEventListener('mouseover', () => {
    let messages = document.querySelectorAll('.NOTIFICA0, .NOTIFICA1, .NOTIFICA2');
    messages.forEach((e, i) => {
        e.addEventListener('click', () => {

            Chat.style.display = 'flex'
            let UTENTE1 = document.querySelector('#UTENTE1')
            let mesUtente1 = document.querySelector('#mesUtente1')
            let UTENTE2 = document.querySelector('#UTENTE2')
            let mesUtente2 = document.querySelector('#mesUtente2')
            let a1 = MES2[i]['Ricevente']
            let a2 = a1.split('@')

            UTENTE1.innerHTML = MES2[i]['Ricevente']
            mesUtente1.innerHTML = MES2[i]['mesRice']
            UTENTE2.innerHTML = MES2[i]['Destinatario']
            mesUtente2.innerHTML = MES2[i]['mesDest']

            document.getElementById('nomeChat').textContent = a2[0]
        })
    });
})
document.querySelector('#creaNotifica').addEventListener('click', () => {
    Chat.style.display = 'flex'
    document.querySelector('#STATO').innerHTML = ''
    document.querySelector('#nomeChat').innerHTML = ''
    document.querySelector('#DISPLAY').innerHTML = ''
    document.querySelector('#attributoMessaggio').style.visibility = 'visible'

})


//MESSAGGI
const lista_amici = []
btnMessaggi.addEventListener('mouseover', () => {
    const linkElements = Array.from(document.querySelectorAll('.AMICI'));
    linkElements[0].style.display = 'none'

    const amici = document.querySelectorAll('.AMICI');
    amici.forEach((e, i) => {
        let friend = e.querySelectorAll('.AMICO');
        friend.forEach((fri) => { lista_amici.push(fri.textContent) })

        e.addEventListener('click', () => {
            Chat.style.display = 'flex'
            document.querySelector('#STATO').innerHTML = 'OFFLINE'
            document.querySelector('#attributoMessaggio').style.visibility = 'hidden'

            let DISPLAY = document.querySelector('#DISPLAY')

            if (DISPLAY.childNodes.length > 0) {
                while (DISPLAY.firstChild) { DISPLAY.removeChild(DISPLAY.firstChild) }
            }

            document.getElementById('nomeChat').textContent = lista_amici[i]

            let contenitori = [];
            (() => {
                let c = []
                c.push(checkChat(lista_amici[i]))

                for (let ab in c[0]) {
                    let count1 = 0
                    let count2 = 0

                    let mesTU = []
                    let mesIO = []
                    let mesTUL = mesTU.length
                    let mesIOL = mesIO.length

                    mesTU.push(c[0][ab]['tu'])
                    mesIO.push(c[0][ab]['io'])

                    aSchermo(count1, mesIOL, User['email'], mesIO, "red", contenitori)
                    aSchermo(count2, mesTUL, Amici[i + 1]['email'], mesTU, "blue", contenitori)
                }
            })()
        })
    });
})
function aSchermo(count, mesLength, CHI, mesCHI, colore, contenitori) {
    while (count <= mesLength) {
        let n = document.createElement('span')
        let mesN = document.createElement('span')
        let br1 = document.createElement('br')
        let br2 = document.createElement('br')

        let a = []
        const E = [n, br1, mesN, br2]

        n.textContent = CHI
        n.style.color = colore
        if (mesCHI[count] != null && mesCHI[count] != 'null' && mesCHI[count] != '') {

            mesN.textContent = mesCHI[count]
            for (const e of E) { DISPLAY.append(e) }
        }
        a.push(n)
        a.push(mesN)
        contenitori.push(a)

        count++
    }
}

//ATTRIBUTO
const AT = document.querySelector('#attributoMessaggio')
AT.addEventListener('change', checkAttributo)
let ATmiaNotifica = []
function checkAttributo() {

    let ATtext = document.querySelector('#attributoMessaggio').value

    if (ATtext == '' || ATtext == ' ') { ATmiaNotifica.push(ATtext) }
    else if (ATtext != 0 && ATtext != 1 && ATtext != 2) { window.alert('non valido') }
    else { ATmiaNotifica.push(ATtext) }
}

//SEND
btn.addEventListener('click', () => {
    let ATtext = document.querySelector('#attributoMessaggio').value

    let risposta = document.querySelector('#USER').value

    const text = document.createElement('span')
    const io = document.createElement('span')
    const br1 = document.createElement('br')
    const br2 = document.createElement('br')

    io.textContent = User['email']
    io.style.color = '#0b0d26'
    io.classList.add('IO')
    text.classList.add('textIO')

    text.textContent = risposta

    const elementi = [io, br1, text, br2]
    for (const elemnto of elementi) { displayChat.append(elemnto) }

    //QUANDO
    const DATA = () => {
        const Y = new Date().getFullYear()
        const M = new Date().getMonth() + 1
        const UTCDate = new Date().getUTCDate()
        const h = new Date().getHours()
        const m = new Date().getMinutes()
        const s = new Date().getSeconds()

        const Data = `${UTCDate}-${M}-${Y} ${h}:${m}:${s}`
        return Data
    }

    //NEL CASO 1 O PIU MESSAGGI
    let a = []
    document.querySelectorAll('.textIO').forEach((e) => { a.push(e.textContent) })

    //MESSAGGIO
    let messaggio = {
        "da": User['nome'],
        "a": document.querySelector('#nomeChat').textContent,
        "messaggio1": a[0],
        "messaggio2": null,
        "quando": DATA(),
        "att": ATmiaNotifica[0]
    }

    // SEND A SERVER
    setTimeout(() => {
        if (aChi && a[0] && messaggio['att'] == undefined) {
            fetch(`/chat/${messaggio['da']}/${messaggio['a']}/${messaggio['messaggio1']}/${messaggio['messaggio2']}/${messaggio['quando']}`)
                .then(res => res.json())
                .then(d => console.log(d))
            ATmiaNotifica = []
        }
        else if (a[0] && messaggio['att'] != undefined) {
            fetch(`/notifica/${messaggio['da']}/${messaggio['messaggio1']}/${messaggio['quando']}/${messaggio['att']}`)
                .then(res => res.json())
                .then(d => console.log(d))
            ATmiaNotifica = []
        }
        else { window.alert('compila tutti i campi necessari') }
    }, 500)
})