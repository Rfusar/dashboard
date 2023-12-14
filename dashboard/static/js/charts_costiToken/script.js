fetch("/dati").then(res => res.json()).then(d =>{
    let s = 0
    for(let i of d[0]){ s+=i}

    let costo = s * 0.004 * 1.335 / 1000
    document.querySelector('#costo').textContent = `TOTALE: €${costo.toFixed(3)}`
})

