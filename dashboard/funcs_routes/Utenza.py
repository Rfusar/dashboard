def LOGIN(request, DB, listaColleghi, session, bcrypt, redirect, url_for):
    try: 
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            check = DB['users'].find_one({"contact.email": email})
            try:
                if check and bcrypt.checkpw(password.encode('utf-8'), check['password']):
                    utenti = listaColleghi(email)
                    #utente
                    for i in utenti: 
                        if i['utente']["contatti"]['email'] == email: 
                            session['utente'] = i
                        else:
                            print("sei un coglione, perche chi cazzo sei???")
                            return redirect(url_for('login'))

                    utenteRuolo = session.get('utente')['ruolo']
                    #colleghi
                    session['users'] = utenti
                    #livello utente
                    session['demo'] = utenteRuolo

                    RUOLI = ["user", "referent", "spike-user", "spike-admin", "admin"]
                    for i in range(len(RUOLI)): 
                        if session.get('utente')['ruoli']['base'] == RUOLI[i]: 
                            return redirect(url_for('HOME'))
                        else:
                            print("sei un coglione, il ruolo non torna")
                            return redirect(url_for('login'))
                else:
                    print("sei un coglione, la password non funziona")
                    return redirect(url_for('login'))
                
            except Exception as e:
                print(str(e)+"errore except")
                return redirect(url_for('login'))
            
    except Exception as e:
        print(str(e))
        return redirect(url_for('login'))

def REGISTER(request, bcrypt, DB, redirect, url_for, dt, Token):
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            cognome = request.form['cognome']
            password = request.form['password']
            RG = request.form['ragionesociale']
            email = request.form['email']
            telefono = request.form['telefono']

            company = DB['companies'].find_one({"name": RG}, {"name": 1, "_id": 1})

            if company['name'].upper() == RG.upper():
                aziendaID = company['_id'] 
                userCode = Token(9)
                password_crypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

                DB['users'].insert_one({
                    "photo": None,
                    "businessRole": "staff",
                    "active": True,
                    "validated": True,
                    "craeteAt": dt.now(),
                    "name": {"firstName": nome, "lastName": cognome},
                    "contact": {"email": email, "phone": telefono},
                    "role": None,
                    "company": aziendaID,
                    "password": password_crypt,
                    "userCode": userCode,
                    "slug": f"{nome}-{cognome}-{userCode}",
                    "passwordChangedAt": None,
                    "passwordResetExpires": None,
                    "passwordResetToken": None,
                    "updateAt": None
                })

                return redirect(url_for('login'))
            else:
                return redirect(url_for('registrazione'))  
    except:...

def reset_password(request, bcrypt, DB, redirect, url_for):
    try:
        if request.method == "POST":
            email = request.form['email']
            password = request.form['new-password']
            token = request.form['token']

            utente = DB['users'].find_one({"email":email})
            if utente.get('passwordResetToken') == token:
                password_crypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
                DB['users'].update_one({"email": email}, {"$set": {"password": password_crypt}})
                return redirect(url_for('login'))
            else:
                return redirect(url_for('resetPassword')) 
    except:...
