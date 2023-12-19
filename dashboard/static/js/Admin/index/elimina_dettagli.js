//DETTAGLI
window.addEventListener('click',()=>{
    document.querySelectorAll('.piu_dettagli').forEach((e, i) => {
        e.addEventListener('click', () => { e.setAttribute("href", `/utente/${document.querySelectorAll('.email_utente')[i].textContent}`) })
    })
    
})


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