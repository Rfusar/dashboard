function setImg(path, e){
    const img = document.createElement('img')
        img.style.width = "25px"
        img.setAttribute('src', path)
        img.setAttribute('alt', 'ruolo')
        e.textContent = ""
        e.append(img)
}

document.querySelectorAll('.ruolo').forEach(e=>{
    if(e.textContent == "admin"){ setImg("../../static/img/admin.png", e)}
    else if(e.textContent == "utente"){ setImg("../../static/img/user.png", e)}
    else if(e.textContent == "superadmin"){ setImg("../../static/img/superadmin.png", e)}
})