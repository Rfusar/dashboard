function setImg(path, e, contenutoDescizione) {
    const img = document.createElement('img')
    const descrizione = document.createElement('abbr')
    descrizione.setAttribute('title', contenutoDescizione)
    descrizione.style.cursor = "default"

    img.style.width = "25px"
    img.setAttribute('src', path)
    img.setAttribute('alt', 'ruolo')
    e.textContent = ""
    descrizione.append(img)
    e.append(descrizione)
}

function SET(e) {
    if (e.textContent == "spike-user") { setImg("../../static/img/admin.png", e, "user-spike") }
    else if (e.textContent == "user") { setImg("../../static/img/user.png", e, "user") }
    else if (e.textContent == "spike-admin") { setImg("../../static/img/superadmin.png", e, "spike-admin") }
    else if (e.textContent == "referent") { setImg("../../static/img/referente.png", e, "referente") }
}

document.querySelectorAll(".ruolo").forEach(e => {SET(e)})
document.querySelectorAll("#ruolo").forEach(e => {SET(e)})


