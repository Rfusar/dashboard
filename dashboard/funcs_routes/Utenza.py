def LOGIN(connPOSTGRES, email, listaColleghi, session, check_password_hash, password, redirect, url_for):
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
        colleghiAzienda = []
        if utenteRuolo == "superadmin":
            for utentiAzienda in utenti: colleghiAzienda.append(utentiAzienda)

        elif utenteRuolo == "admin":
            for utentiAzienda in utenti: colleghiAzienda.append(utentiAzienda) if utentiAzienda['ruolo'] != "superadmin" else None    

        elif utenteRuolo == "utente":
            for utentiAzienda in utenti: colleghiAzienda.append(utentiAzienda) if utentiAzienda['ruolo'] == "utente" else None     

        session['users'] = colleghiAzienda

        #livello utente
        session['demo'] = utenteRuolo
            
        if check_password_hash(u[0][0], password):
            #INDIRIZZAMENTO A PAGINA PRINCIPALE
            ruoli = ["utente", "admin", "superadmin"]
            for i in range(len(ruoli)): 
                if session.get('utente')['ruolo'] == ruoli[i]: return redirect(url_for('HOME'))   
  
        else:
            return redirect(url_for('login'))
            
    except:
        return redirect(url_for('login'))
    

def REGISTER(generate_password_hash, password, connPOSTGRES, redirect, url_for, nome, cognome, telefono, RG, email):
    p = generate_password_hash(password)

    try:    
        cur = connPOSTGRES.cursor()
        cur.execute("insert into utenti (nome, cognome, tel, ragionesociale, email, password) values (%s,%s,%s,%s,%s,%s)",(nome, cognome, telefono, RG, email, p))
        connPOSTGRES.commit()
        cur.execute("insert into ruoli (email, ragionesociale, livello) values (%s, %s, 'utente')", (email, RG))
        connPOSTGRES.commit()
        cur.close()
        return redirect(url_for('login'))
    
    except Exception as e:
        print(str(e))
        return redirect(url_for('registrazione'))  

def reset_password(generate_password_hash, password, connPOSTGRES, email, redirect, url_for):
    #aggiungere funzionalita con SMS oppure email
    p = generate_password_hash(password)
    try:
        cur = connPOSTGRES.cursor()

        cur.execute("UPDATE utenti SET password = %s WHERE email = %s", (p, email))
        connPOSTGRES.commit()
        cur.close()
        return redirect(url_for('login'))

    except:
        return redirect(url_for('resetPassword')) 

