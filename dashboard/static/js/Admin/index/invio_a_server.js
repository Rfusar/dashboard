function manda_a_SERVER(path, oggetto) {
    if (path == "/modificaDB") {
        fetch(path, {
            method: 'POST',
            body: JSON.stringify(oggetto),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(res => res.json()).then(d => {
                document.querySelector('#risposte').innerHTML = ""
                for(const res of d){
                    const p = document.createElement('p')
                    p.textContent = res
                    document.querySelector('#risposte').append(p)
                }
            })
    }

}