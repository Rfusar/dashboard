//REGOLE
let a = document.querySelector('#System')
a.addEventListener("input", () => {
    if (a.value.length > 16000) {
        window.alert("messaggio troppo lungo")
        a.value = ""
    }
})



//DECISIONE COSTO per 1K token
let tot = document.querySelector("#costo").textContent * 1.335
document.querySelector("#costo").textContent = tot
//perche calcolo in base al nostro prezzo
costo_di_un_token = tot / 1000


//CERCA FILE
document.getElementById('leggiFileButton').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const contenuto = event.target.result;
            file_nome = file.name
            let oggetto = {
                "nome": file.name,
                "file": contenuto
            }

            fetch('/carica_file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(oggetto)
            })
                .then(res => res.json())
                .then(d => {
                    costo_documento = d["token"]["SYSTEM"]['scritto su file']["cl100k_base"] * costo_di_un_token
                    document.querySelector('#System').textContent = d['testo'];
                    document.querySelector("#Token").textContent = d["token"]["SYSTEM"]['scritto su file']["cl100k_base"]
                    document.querySelector("#char").textContent = document.querySelector('#System').textContent.length
                    document.querySelector("#COSTO").textContent = `€${costo_documento.toFixed(3)} + costo di lavorazione`
                    document.querySelector("#compila").classList.remove("disabled")
                    //check
                    document.querySelector('#aspettaCheck').textContent = "STATUS: pronto?, COMPILA e aspetta 20 sec"
                })
                .catch(error => {
                    console.error('Errore:', error);
                });
        };
        reader.readAsText(file);
        attivazione_compila_file()

    } else {
        alert('Nessun file selezionato.');
    }
    console.log(document.querySelector("#User").textContent)
});
function attivazione_compila_file() {
    document.querySelector('#compila').addEventListener('click', () => {
        oggetto = {
            "nome": file_nome,
            "comando": document.querySelector("#User").value,
            "file": document.querySelector('#System').textContent
        }

        fetch('/carica_file2', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(oggetto)
        })
            .then(res => res.json()).then(d => {
                document.querySelector('#aspettaCheck').textContent = `STATUS: ${d['status']}`
            })
    })
}




//CERCA CARTELLA
const documenti = []
class Cartella {
    constructor(titolo, contenuto, token) {
        this.titolo = titolo
        this.contenuto = contenuto
        this.token = token
    }
    lavorazione(array) {
        array.push({
            "titolo": this.titolo,
            "contenuto": this.contenuto,
            "token": this.token,
        })
    }
}
document.getElementById('leggiCartellaButton').addEventListener('click', () => {
    const cartellaInput = document.getElementById('cartellaInput');
    const files = cartellaInput.files;

    if (files.length > 0) {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }
        fetch('/carica_folder', {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(d => {
                for (let i of d) {
                    new Cartella(i['documento']['nome'], i['documento']['contenuto'], i['documento']['token']).lavorazione(documenti)
                }
                let token = 0
                let caratteri = 0
                for (let i of d) {
                    token += i['documento']['token']
                    caratteri += i['documento']['n_char']
                }
                let costo = costo_di_un_token * token

                document.querySelector("#Token").textContent = token
                document.querySelector("#char").textContent = caratteri
                document.querySelector("#COSTO").textContent = `€${costo.toFixed(3)} + costo di lavorazione`
                document.querySelector("#compilaCartellaButton").classList.remove("disabled")
            })

        attivazione_compila_cartella()
    }
})
function attivazione_compila_cartella() {
    document.getElementById('compilaCartellaButton').addEventListener('click', () => {
        ogg = { 
            "comando": document.querySelector("#User").value,
            'documenti': documenti 
        }
        fetch('/carica_folder2', {
            method: 'POST',
            headers: { 'content-Type': 'application/json' },
            body: JSON.stringify(ogg)
        })
            .then(res => res.json())
            .then(d => {
                document.querySelector('#aspettaCheck').textContent = `STATUS: ${d['status']}`
            })
    })
}



