from dashboard import app
from flask import render_template,jsonify,request,session, redirect, url_for
from database.DB import connPOSTGRES
from database.DBchat import chat, readChat,notifica, readNotifica, allNotifica
from database.DBuser import listaColleghi
from functools import wraps
#from .classDefinition import RegistrazioneForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
#funzioni_per_semplificare
from dashboard.funcs_routes.funcs1 import checkMese, Documenti__da_DB
from dashboard.funcs_routes.Utenza import LOGIN, REGISTER, reset_password
from dashboard.funcs_routes.Pagine_principali import principale___utente, principale___admin, principale__superadmin
from dashboard.funcs_routes.API import API___azienda, API___utente


#*START
@app.route("/")
def home():
    session['demo'] = True
    return render_template('index.html', check = True)
    
    


#*************************************************************************************************** UTENZA
#-----> registrazione
@app.route("/registrazione")
def registrazione(): return render_template("user/register.html")

@app.route("/fetchRegister", methods=["POST"])
def logicaRegistrazione():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        password = request.form['password']
        RG = request.form['ragionesociale']
        email = request.form['email']
        telefono = request.form['telefono']

        return REGISTER(generate_password_hash, password, connPOSTGRES, redirect, url_for, nome, cognome, telefono, RG, email)

#-----> login 
@app.route("/login")
def login(): return render_template("user/login.html")

@app.route("/fetchUtente", methods=["POST"])
def logicaLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 
        try:
            return LOGIN(connPOSTGRES, email, listaColleghi, session, check_password_hash, password, redirect, url_for)
        except Exception as e:
            print(str(e))
           
#-----> resetPassword
@app.route("/resetPassword")
def resetPassword(): return render_template("user/forgot-password.html")

@app.route("/fetchResetPassword", methods=["POST"])
def logicaResetPassword(email, password):
    if request.method == "POST":
        return reset_password(generate_password_hash, password, connPOSTGRES, email, redirect, url_for)
  
#LOGOUT
@app.route('/logout')
def logout():
    session['utente'] = None
    session['users'] = None
    session['messaggi'] = None
    session['demo'] = True
    return redirect(url_for('home'))


#*************************************************************************************************** UTENTE
@app.route("/HOME")
def HOME():
    if session.get('demo') == "utente":
        return principale___utente(session, readChat, allNotifica, readNotifica, connPOSTGRES, dt, render_template, checkMese)
    
    elif session.get('demo') == "admin":
        return principale___admin(session, connPOSTGRES, render_template)
    
    elif session.get('demo') == "superadmin":
        return principale__superadmin(session, render_template)

#PAGINE
@app.route("/charts")
def charts():
    if session.get('demo') == "utente" or session.get('demo') == "admin":
        u = session.get('utente')
        users = session.get('users')
        demo = session.get('demo')
        try: 
            l=len(session['notifica'][0]['altri'])
        except: l = 0
        usersL = len(users)

        nome = u['utente'][0]
        return render_template("charts.html",Nmes = l, amici = users, N_amici =usersL -1, nome=nome, check = demo, ragionesociale=u['azienda'])
    
    elif session.get('demo') == True:
        return render_template("charts.html", check = True)

#--------> GRAFICO 
@app.route("/dati")
def dati():
    MESI = ["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
    links=[1000,1200,1300,1500,1200,1700,1200,1400,1100,1200,1300,1200]
    
    return jsonify(links, MESI)

#--------> TABELLE   
@app.route("/tableInfo", methods=["GET","POST"])
def tableInfo():
    DATI = {}

    cur = connPOSTGRES.cursor()
    DOCUMENTI_MUTUI = Documenti__da_DB(cur, session, "MUTUI")
    DATI['documenti_mutuo'] = DOCUMENTI_MUTUI
    cur.close()

    return jsonify(DATI)

@app.route("/table")
def table():
    if session.get('demo') == "utente" or session.get('demo') == "admin":
        u = session.get('utente')
        users = session.get('users')
        demo = session.get('demo')

        try:
            l=len(session['notifica'][0]['altri'])
        except: l = 0
        usersL = len(users)

        cur = connPOSTGRES.cursor()
        links = Documenti__da_DB(cur, session, "MUTUI")
        cur.close()

        return render_template("tables.html",Nmes = l, amici = users, N_amici =usersL -1, links = links, nome = u['utente'][0], check= demo, ragionesociale=u['azienda'])

    elif session.get('demo') == True:
            return render_template("tables.html", check=True)

#--------> CHECK UTENTI
@app.route("/listaColleghi")
def utenti___superadmin(): 
    if session.get('demo') == "admin" or session.get('demo') == "superadmin":
        u = session.get('utente')
        users = session.get('users')
        demo = session.get('demo')

        link = []
        if session.get("demo") == "admin":
            for i in users: 
                if i['utente'][0] == u['utente'][0]: continue    
                utente = [i['utente'][0], i['utente'][1], i['email'], i['ruolo']]
                link.append(utente)
        elif session.get("demo") == "superadmin":
            for i in users: 
                if i['utente'][0] == u['utente'][0]: continue    
                utente = [i['azienda'], i['utente'][0], i['utente'][1], i['email'], i['ruolo']]
                link.append(utente)


        try:
            l=len(session.get('notifica')[0]['altri'])
        except: l = 0
        usersL = len(users)


    return render_template("Admin/tabelleUtenti.html",
                           Nmes = l, 
                           amici = users, 
                           N_amici =usersL -1, 
                           nome=u['utente'][0], 
                           check = demo,
                           links = link,
                           ragionesociale=u['azienda']
                           )


#---------> MESSAGGI
#CHAT
@app.route("/chat/<a>/<b>/<c>/<d>/<e>", methods=['GET'])
def a(a,b,c,d,e):
    
    A = a
    B = b
    C = c
    D = d
    E = e
 
    chat(a,b,c,d,e)

    abc = {
        'A0': A,
        'A1': B,
        'A2': C,
        'A3': D,
        'A5': E
    }
    return jsonify([abc])

#NOTIFICA
@app.route("/notifica/<a>/<b>/<c>/<d>", methods=['GET'])
def b(a,b,c,d):
    azienda = session.get('UTENTE')
    A = a
    B = b
    C = c
    D = d

    notifica(a,b,c,d,azienda['azienda'])

    abc = {
        'A0': A,
        'A1': B,
        'A2': C,
        'A3': D,
        "A4":azienda['azienda']  
    }

    return jsonify([abc])



#*************************************************************************************************** ADMIN
@app.route("/adminCheck")
def adminCheck():
    if session.get('demo') == "admin":
        nomeAzienda = session.get('utente')['azienda']

        #CHECK CHAT
        cur = connPOSTGRES.cursor()
        cur.execute('SELECT nome FROM utenti WHERE ragionesociale = %s', (nomeAzienda,))
        nomiUSERS = cur.fetchall()

        cur.execute("SELECT token FROM documenti WHERE ragionesociale = %s", (nomeAzienda,))
        tokenAll = cur.fetchall()

        try:
            CHAT = {}
            for i in range(0, len(nomiUSERS)):
                if  i == len(nomiUSERS)-1: 
                    CHAT['chat'] = readChat(nomiUSERS[0][0], nomiUSERS[i][0])
                CHAT['chat'] = readChat(nomiUSERS[i+1][0], nomiUSERS[i][0])
        except:...

        token = 0

        for i in tokenAll:
            token += i[0]

        result ={
            'utenti':nomiUSERS,
                'chat':CHAT,
            'token': token
           }
    

        return jsonify(result)
    
    else: return {"mess": "non puoi"}



#*************************************************************************************************** SUPERADMIN
@app.route("/superadminCheck")
def superadminCheck():
    if session.get('demo') == "superadmin":
        #CHECK CHAT
        cur = connPOSTGRES.cursor()
        cur.execute('SELECT nome, cognome, email, ragionesociale FROM utenti')
        nomiUSERS = cur.fetchall()
        cur.execute("SELECT nome, livello FROM ruoli")
        ruoli = cur.fetchall()
        #finire
        for i in range(len(ruoli)):
            ...
        try:
            CHAT = {}
            for i in range(0, len(nomiUSERS)):
                if  i == len(nomiUSERS)-1: 
                    CHAT['chat'] = readChat(nomiUSERS[0][0], nomiUSERS[i][0])
                CHAT['chat'] = readChat(nomiUSERS[i+1][0], nomiUSERS[i][0])
        except:...

        cur.execute("SELECT token, ragionesociale FROM documenti")
        tokenAll = cur.fetchall()
        #SOMMA TOTALE
        token = 0
        for i in tokenAll: token += i[0]
        

        cur.execute("SELECT * FROM azienda")
        aziende = cur.fetchall()
        cur.close()

        result ={
            'utenti':nomiUSERS,
            'chat':CHAT,
            'tokenTOT': token,
            'token':  tokenAll,
            'aziende': aziende
           }
        
        return jsonify(result)
    
    else: return {"mess": "non puoi"}


@app.route("/Tickets")
def Ticket():
    u = session.get('utente')
    users = session.get('users')

    try:
        l=len(session['notifica'][0]['altri'])
    except: l = 0
    usersL = len(users)
    nome = u['utente'][0]
    demo = session.get('demo')

    return render_template("/tickets.html",Nmes = l, amici = users, N_amici =usersL -1, links = [], nome = nome, check= demo, ragionesociale=u['azienda'])


#CHECK AZIENDE
@app.route("/superadmin/aziende")
def aziende___superadmin(): 
    if session.get('demo') == "superadmin":
        demo = session.get('demo')
        u = session.get('utente')
        users = session.get('users')

        cur = connPOSTGRES.cursor()
        cur.execute("SELECT * FROM azienda")
        aziende = cur.fetchall()

        try:
            l=len(session.get('notifica')[0]['altri'])
        except:l =0
        usersL = len(users)
        return render_template("Admin/tabelleAziende.html", 
                                Nmes = l, 
                                amici = users, 
                                N_amici =usersL -1, 
                                nome=u['utente'][0],
                                check = demo,
                                links = aziende,
                                ragionesociale=u['azienda']
                                )

@app.route("/superadmin/checkAziende", methods=["POST"])
def check_aziende___superadmin():
    if session.get('demo') == "superadmin":
        try:
            cur = connPOSTGRES.cursor()
            cur.execute("SELECT * FROM azienda")
            aziende = cur.fetchall()
            return jsonify(aziende)
        except Exception as e:
            return jsonify(str(e))


@app.route("/superadmin/report")
def report___superadmin():
    return render_template("Admin/report.html")



#*************************************************************************************************** ALTRO
#Help
@app.route("/Help", methods=['GET'])
def HELP():
    u = session.get('utente')
    demo = session.get('demo')
   
    try: 
        l=len(session['notifica'][0]['altri'])
    except: l = 0
    
    amici = session.get('users')
    N_amici = len(amici)

    return render_template('componenti/Help.html',
                        check = demo, 
                        nome= u['utente'][0], 
                        cognome=u['utente'][1], 
                        email=u['email'], 
                        messaggio=session.get('notifica')[0]['altri'],
                      
                        Nmes = l,
                        amici = amici,
                        N_amici =N_amici -1)  

#Prove
@app.route("/modificaDB", methods=['POST'])
def prova():
    dati = request.json
    risposte = []
    cur = connPOSTGRES.cursor()

    for utente in dati:
        azienda = utente.get('azienda')
        nome = utente.get('nome')
        cognome = utente.get('cognome')
        email = utente.get('email')
        modifica = utente.get('modifica')
        elimina = utente.get('elimina')

        check = ""
        #superadmin
        if session.get("demo") == "superadmin": 
            if elimina:
                #cur.execute("DELETE FROM utenti WHERE nome = %s and cognome = %s and email = %s", (nome, cognome, email))
                #cur.execute("DELETE FROM ruoli WHERE nome = %s and ragionesociale = %s", (nome, azienda))
                check += "eliminato"

            elif  modifica:
                #cur.execute("UPDATE ruoli SET livello = 'admin' WHERE nome = %s and cognome = %s and email = %s", (nome, cognome, email))
                check += "reso admin"

            risposta = f"L'utente {nome} {cognome}, lavora presso: {azienda}; {check} con successo"
            risposte.append(risposta)

    cur.close()
    return jsonify(risposte)

#Check
@app.route("/messaggi", methods=['GET'])
def mes():
    try:
        u = session.get('utente')
        m = session.get('chat')
        a = session.get('users')
        a1 = session.get('notifica')
        c1 = session.get('demo')
        
        return jsonify(u, m, a, a1, c1)
    
    except: return {"Ti è andata male"}


#capacita d'interagire con DB
def requires_auth(f):
    def check_credentials(username, password):
        return username == "ricky" and password == "password"
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            return ('Credenziali non valide. Effettua il login.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    
    return decorated

@app.route("/check/dati", methods=['POST'])
def checkDati():
    query = request.json
    cur = connPOSTGRES.cursor()
    try:
        cur.execute(query['query'])
        res =  cur.fetchall()
        return jsonify(res)
    
    except: return {"errore": "query non eseguita"}


@app.route('/check/provaAuth')
@requires_auth
def pagina_protetta():
    return render_template("Admin/sql.html")



#*************************************************************************************************** API
@app.route("/registrazione_azienda", methods=['POST'])
def registrazione_azienda_api(): return API___azienda(request, connPOSTGRES)


@app.route("/registrazione_utente", methods=['POST'])
def registrazione_utente_api(): return API___utente(request, generate_password_hash, connPOSTGRES)

'''
COSE DA FARE:
    -

APPUNTI:
    - /dati -> GRAFICO ---> utente, admin, superadmin
'''