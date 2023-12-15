def principale___utente(session, readChat, allNotifica, readNotifica, connPOSTGRES, dt, render_template, checkMese):
    #PRELIEVO CHAT
    amici = session.get('users')
    u = session.get('utente')
    demo = session.get('demo')

    CHAT = []
    NOTIFICA = []

    for i in amici:
        ogg1={}
        ogg2={}

        ogg1['chat'] = readChat(u['utente'][0], i['utente'][0])

        ogg2['altri'] = allNotifica(u['azienda'])
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
                       title="IRON_BOX-dashboard",
                       check = demo, 
                       nome = u['utente'][0], 
                       cognome = u['utente'][1], 
                       email = u['email'], 
                       messaggio=notifiche,
                      
                       ragionesociale = u['azienda'],
                       Nmes = l,
                       amici = amici,
                       N_amici =N_amici -1,

                        anno = dt.now().year
                       )

def principale___admin(session, connPOSTGRES, render_template):
    u = session.get('utente')
    users = session.get('users')
    demo = session.get('demo')

    cur = connPOSTGRES.cursor()
    cur.execute('SELECT email, livello FROM ruoli WHERE ragionesociale = %s', (u['azienda'],))
    access = cur.fetchall()
    cur.close()

    link = []
    for utente in users:
        for ruoli in access:
            if utente['email'] != u['email'] and utente['utente'][0] == ruoli[0] and ruoli[1] != "superadmin":
                link.append([utente['utente'][0], utente['utente'][1], utente['email'], ruoli[1]])

    try:
        l=len(session.get('notifica')[0]['altri'])
    except: l = 0
    usersL = len(users)

    return render_template("base.html",
                       title="IRON_BOX-dashboard",
                       Nmes = l, 
                       amici = users, 
                       N_amici =usersL -1, 
                       nome=u['utente'][0], 
                       check = demo,
                       links = link,
                       ragionesociale = u['azienda']
                       )    

def principale__superadmin(session, render_template):
    if session.get('demo') == "superadmin":
        u = session.get('utente')
        users = session.get('users')
        demo = session.get('demo')

        try:
            l=len(session.get('notifica')[0]['altri'])
        except: l = 0
        
        usersL = len(users)

    return render_template("charts.html",
                           title="IRON_BOX-dashboard",
                           Nmes = l, 
                           amici = users, 
                           N_amici =usersL -1, 
                           nome= u['utente'][0], 
                           check = demo,
                           ragionesociale=u['azienda']
                           )