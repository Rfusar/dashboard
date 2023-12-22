from datetime import datetime as dt
years = [[dt.now().year], [dt.now().year-1], [dt.now().year-2], [dt.now().year-3]]
docs = [["id1", "title1", "category1", "2023", "tag1", "img", "22/10/2023"],
        ["id1", "title1", "category1", "2023", "tag1", "img", "22/10/2023"],
        ["id1", "title1", "category1", "2023", "tag1", "img", "22/10/2023"],
        ["id1", "title1", "category1", "2023", "tag1", "img", "22/10/2023"],
        ["id1", "title1", "category1", "2023", "tag1", "img", "22/10/2023"]]


def principale___utente(session, readChat, allNotifica, readNotifica, dt, render_template, checkMese, DB):
    if session.get('demo') == "utente":
        amici = session.get('users')
        u = session.get('utente')

        CHAT = []
        NOTIFICA = []

        for i in amici:
            ogg1={}
            ogg2={}

            ogg1['chat'] = readChat(u['utente'][0], i['utente'][0])

            ogg2['altri'] = allNotifica(u['azienda'], DB)
            ogg2['mia'] = readNotifica(i['utente'][0], u['azienda'])
        
            CHAT.append(ogg1)
            NOTIFICA.append(ogg2)
    

        session['chat'] = CHAT
        session['notifica'] = NOTIFICA   

        notifiche = session.get('notifica')[0]['altri']
        try:
            l=len(notifiche)
        except: l = 0
        N_amici = len(amici)


    
        return render_template('base.html',
                       title="Repository_GDPR",
                       check = session.get("demo"), 
                       ruolo = session.get("demo"), 
                       nome = u['utente'][0], 
                       cognome = u['utente'][1], 
                       email = u['email'], 
                       messaggio=notifiche,

                       years = years,
                       docs = docs,
                      
                       ragionesociale = u['azienda'],
                       Nmes = l,
                       amici = amici,
                       N_amici =N_amici -1,
                        mese = checkMese(dt),
                        anno = dt.now().year
                       )

def principale___admin(session, render_template, dt, checkMese):
    u = session.get('utente')
    users = session.get('users')
    demo = session.get('demo')

    link = []
    for utente in users:
        link.append([
            utente['utente']['idetificazione']['nome'], 
            utente['utente']['idetificazione']['cognome'], 
            utente['utente']['contatti']['email'], 
            utente['ruoli']['base']
        ])

    try:
        l=len(session.get('notifica')[0]['altri'])
    except: l = 0
    usersL = len(users)

    return render_template("base.html",
                       title="Repository_GDPR",
                       Nmes = l, 
                       amici = users, 
                       N_amici =usersL -1, 
                       ruolo = session.get("demo"), 
                       nome=u['utente'][0], 
                       check = demo,
                       links = link,

                        years = years,
                        docs = docs,

                       ragionesociale = u['azienda'],
                       mese = checkMese(dt),
                       anno = dt.now().year
                       )    

def principale__superadmin(session, render_template, dt, checkMese):
    if session.get('demo') == "superadmin":
        u = session.get('utente')
        try:
            l=len(session.get('notifica')[0]['altri'])
        except: l = 0
        
        usersL = len(session.get('users'))

    return render_template("base.html",
                           title="Repository_GDPR",
                           Nmes = l, 

                           years = years,
                           docs = docs,

                           amici = session.get('users'), 
                           N_amici =usersL -1, 
                           nome= u['utente'][0], 
                           ruolo = session.get("demo"), 
                           check = session.get('demo'),
                           ragionesociale=u['azienda'],
                           mese = checkMese(dt),
                           anno = dt.now().year
                           )