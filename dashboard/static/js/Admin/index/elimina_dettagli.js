gestione___modificaANDdettagli(".modifica", "modifica")
gestione___modificaANDdettagli(".piu_dettagli", "utente")

//ELIMINA
document.querySelectorAll('.elimina').forEach((e, i) => {
    e.addEventListener('click', () => {
        const R = window.confirm("sei sicuro di eliminare l'utente?")
        if (R) {
            fetch("/modificaDB", {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    "email": document.querySelectorAll('.email_utente')[i].textContent,
                    "elimina": true
                })
           }).then(res => res.json()).then(d => { document.querySelector('#risposta').textContent = `${d}... aggiorna la pagina` })
        }
    })
})


function gestione___modificaANDdettagli(classe, pathFisso){
    window.addEventListener('click', ()=>{
        document.querySelectorAll(classe).forEach((e, i)=>{
            e.addEventListener('click', () => { e.setAttribute("href", `/${pathFisso}/${document.querySelectorAll('.email_utente')[i].getAttribute("value")}`) })
        })
    }) 
}