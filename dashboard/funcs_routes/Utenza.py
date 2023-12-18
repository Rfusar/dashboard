def LOGIN(request, connPOSTGRES, listaColleghi, session, check_password_hash, redirect, url_for):
    try: 
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            try:
                cur = connPOSTGRES.cursor()
        
                cur.execute("SELECT password, email FROM utenti WHERE email = %s", (email,))
                u = cur.fetchall()
                cur.execute("SELECT nome, ragionesociale FROM utenti WHERE password = %s", (u[0][0],))
                a = cur.fetchall()

                utenti = listaColleghi(a[0][1], email)
                #utente
                for i in utenti: 
                    if i['email'] == email: session['utente'] = i

                utenteRuolo = session.get('utente')['ruolo']
                #colleghi
                for i in utenti:
                    if utenteRuolo == "superadmin": 
                        session['users'] = utenti

                    elif utenteRuolo == "admin":
                        colleghiAzienda = []
                        for utentiAzienda in utenti:
                            if utentiAzienda['ruolo'] != "superadmin":
                                colleghiAzienda.append(utentiAzienda)
                        session['users'] = colleghiAzienda

                    elif utenteRuolo == "utente":
                        colleghiAzienda = []
                        for utentiAzienda in utenti:
                            if utentiAzienda['ruolo'] == "utente":
                                colleghiAzienda.append(utentiAzienda)
                        session['users'] = colleghiAzienda

                #livello utente
                session['demo'] = utenteRuolo
            
                if check_password_hash(u[0][0], password):
                    #INDIRIZZAMENTO A PAGINA PRINCIPALE
                    ruoli = ["utente", "admin", "superadmin" ]
                    for i in range(len(ruoli)): 
                        if session.get('utente')['ruolo'] == ruoli[i]: return redirect(url_for('HOME'))   
  
                else:
                    return redirect(url_for('login'))
            
            except:
                return redirect(url_for('login'))
    except:...
    


def REGISTER(request, generate_password_hash, connPOSTGRES, redirect, url_for):
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            cognome = request.form['cognome']
            password = request.form['password']
            RG = request.form['ragionesociale']
            email = request.form['email']
            telefono = request.form['telefono']

            p = generate_password_hash(password)

            try:    
                cur = connPOSTGRES.cursor()
                cur.execute("insert into utenti (nome, cognome, tel, ragionesociale, email, password) values (%s,%s,%s,%s,%s,%s)",(nome, cognome, telefono, RG, email, p))
                connPOSTGRES.commit()
                cur.execute("insert into ruoli (nome, ragionesociale, livello) values (%s, %s, 'utente')", (nome, RG))
                connPOSTGRES.commit()
                cur.close()
                return redirect(url_for('login'))

            except:
                return redirect(url_for('registrazione'))  
    except:...

def reset_password(request, generate_password_hash, connPOSTGRES, redirect, url_for):
    #aggiungere funzionalita con SMS oppure email
    try:
        if request.method == "POST":
            email = request.form['email']
            password = request.form['new-password']

            p = generate_password_hash(password)
            try:
                cur = connPOSTGRES.cursor()
                cur.execute("UPDATE utenti SET password = %s WHERE email = %s", (p, email))
                connPOSTGRES.commit()
                cur.close()
                return redirect(url_for('login'))

            except:
                return redirect(url_for('resetPassword')) 
    except:... 