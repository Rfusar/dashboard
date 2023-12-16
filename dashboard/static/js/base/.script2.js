const connChat = () => {
    class chatAmico {
        constructor(tu, io) {
            this.tu = tu,
                this.io = io
        }
    }

    let chat = []
    for (let x in Amici) {
        for (let y in chat_attive) {
            if (chat_attive[y]['chat'] !== null) {
                for (let z in chat_attive[y]['chat']) {
                    if (chat_attive[y]['chat'][z][`${Amici[x]['nome']}`] !== undefined) {
                        const amicoNome = Amici[x]['nome'];
                        if (amicoNome !== User['nome']) {
                            const f = new chatAmico(chat_attive[y]['chat'][z][amicoNome], chat_attive[y]['chat'][z][User['nome']]);

                            if (!chat[amicoNome]) {
                                chat[amicoNome] = [];
                            }
                            chat[amicoNome].push(f);

                        }
                    }
                }
            }
        }
    }
    return chat
}

const checkChat = (utente) => {
    a = connChat()
    if (a[utente]) {
        return a[utente]
    }
}

window.addEventListener('load', () => {
    if (User['nome'] == 'ricky') {
        document.addEventListener("keydown", (event) => {

            if (event.ctrlKey && event.key == 'à') {
                fetch('/CHECKPROVA')
                    .then(response => response.json())
                    .then(data => {

                        console.log(data);
                        console.log(connChat());

                    })
                    .catch(error => {
                        console.error('Si è verificato un errore:', error);
                    });

            }

            if (event.ctrlKey && event.key == 'è') {
                document.querySelectorAll('.AMICO').forEach((e) => {

                    console.log(chat_attive)
                    console.log(notifiche_attive)
                    console.log(Amici)
                    console.log(User)
                    console.log('')
                    console.log('lavoro di dati')
                    console.log(connChat())
                    console.log('chat')
                    for (let i in Amici) {
                        console.log(checkChat(Amici[i]['nome']))
                    }
                    console.log('dati totali')
                    console.log(d)
                })


            }

            if (event.ctrlKey && event.key == 'ù') {
                fetch('/check/provaAuth')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Errore nella risposta dalla richiesta');
                        }
                        return response.text(); // o response.json() se la risposta è JSON
                    })
                    .then(data => {
                        // Apri una nuova finestra o scheda con il contenuto HTML ricevuto
                        const nuovaFinestra = window.open('', '_blank');
                        nuovaFinestra.document.write(data);
                    })


                    .catch(error => {
                        console.error('Si è verificato un errore:', error);
                    });

            }

        });
    }
})