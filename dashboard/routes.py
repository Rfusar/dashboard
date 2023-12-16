from dashboard import app
from flask import render_template,jsonify,request,session, redirect, url_for
from database.DB import connPOSTGRES, checkToken
from database.DBchat import chat, readChat,notifica, readNotifica, allNotifica
from database.DBuser import listaColleghi
import re
from functools import wraps
#from .classDefinition import RegistrazioneForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from dashboard.interazioneGPT.my_tt import N_token_cl100k_base #USER_GPT
from dashboard.interazioneGPT.connGPT import interact_with_chatgpt_prova
from datetime import datetime as dt
#funzioni_per_semplificare
from dashboard.funcs_routes.funcs1 import checkMese, Documenti__da_DB, Query, modify_DB
from dashboard.funcs_routes.Utenza import LOGIN, REGISTER, reset_password
from dashboard.funcs_routes.Pagine_principali import principale___utente, principale___admin, principale__superadmin
from dashboard.funcs_routes.Documenti_a_chatGPT import lavorazione_foglio, lavorazione_folder, dare_foglio, dare_folder
from dashboard.funcs_routes.API import API___azienda, API___utente, API___documento


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

        return LOGIN(connPOSTGRES, email, listaColleghi, session, check_password_hash, password, redirect, url_for)
           
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


#*************************************************************************************************** PRINCIPALE
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

        l=len(session['notifica'][0]['altri'])
        usersL = len(users)

        nome = u['utente'][0]
        return render_template("charts.html",Nmes = l, amici = users, N_amici =usersL -1, nome=nome, check = demo, ragionesociale=u['azienda'])
    
    elif session.get('demo') == True:
        return render_template("charts.html", check = True)

#--------> GRAFICO 
@app.route("/dati")
def dati():
    MESI = ["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
    if session.get('demo') == "utente" or session.get('demo') == "admin":
        cur = connPOSTGRES.cursor()
        cur.execute("SELECT token, data FROM documenti WHERE ragionesociale = %s",(session.get('utente')['azienda'], ))
        dati = cur.fetchall()
        cur.close()
        
        ultimo_check = checkToken(dati, MESI)    
        return jsonify(ultimo_check, MESI)
    
    elif session.get("demo") == "superadmin":
        cur = connPOSTGRES.cursor()
        cur.execute("SELECT token, data FROM documenti")
        dati = cur.fetchall()
        cur.close()
        
        ultimo_check = checkToken(dati, MESI)    
        return jsonify(ultimo_check, MESI)

    
    elif session.get('demo') == True:
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

        try:
            l=len(session['notifica'][0]['altri'])
        except: l = 0
        usersL = len(users)
        nome = u['utente'][0]
        demo = session.get('demo')

        cur = connPOSTGRES.cursor()
        links = Documenti__da_DB(cur, session, "MUTUI")
        cur.close()
        return render_template("tables.html",Nmes = l, amici = users, N_amici =usersL -1, links = links, nome = nome, check= demo, ragionesociale=u['azienda'])

    elif session.get('demo') == True:
            return render_template("tables.html", check=True)

@app.route("/catalogo")
def catalogo():
    if session.get('demo') == "utente" or session.get('demo') == "admin":
        users = session.get('users')
        l=len(session['notifica'][0]['altri'])
        usersL = len(users)
        demo = session.get('demo')
        u = session.get('utente')
        '''        
        try:
            cur = connPOSTGRES.cursor()
            cur.execute("""
            SELECT 
                documento->>'id',
                documento->>'dataDocumento',
                documento->>'tipo',
                documento->>'nomeAzienda',
                documento->>'aziendaCode',
                documento->>'status',
                documento->>'sapResponse',
                documento->>'officeCode',
                documento->>'act'
            FROM documenti
            """)
            links = cur.fetchall()
            cur.close()
        


        except:
            return render_template("informazioni/404.html")
        '''


        return render_template("catalogo.html",Nmes = l, amici = users, N_amici =usersL -1, nome=u['utente'][0],check=demo, ragionesociale=u['azienda']) #links = links
    
    elif session.get('demo') == True:
        return render_template("catalogo.html",check=True)


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


#---------------------------------------------------------------------------------------------------> TOKENIZER
api_key = ""
maxContent = 4000
creativita = 0

#func file 
@app.route('/carica_file2', methods=['POST'])
def carica_file2():
    documento = request.json
    if documento:
        TITOLO = documento.get('nome')[:-4]
        user_gpt = documento.get('comando')
        system_gpt = documento.get('file')
        dare_foglio(system_gpt, user_gpt, TITOLO)

    else:
        return {"errore":"File non valido"}

@app.route('/carica_file', methods=['POST'])
def carica_file():
    documento = request.json
    if documento:
        testo = documento.get("file")
        lavorazione_foglio(re, testo, N_token_cl100k_base)
    else:
        return {"errore": "Nessun file selezionato."}

#func cartella
@app.route('/carica_folder2', methods=['POST'])
def carica_folder2():
    dati = request.json
    #TEMPO
    return dare_folder(dati)
    
@app.route('/carica_folder', methods=['POST'])
def carica_folder():
    try: 
        lavorazione_folder(request, re, N_token_cl100k_base, jsonify)
    except Exception as e: return {'status': str(e)}

#pagina
@app.route("/token")
def token():
    if session.get('demo') == "utente" or session.get('demo') == "admin":
        u = session.get('utente')
        users = session.get('users')
        demo = session.get('demo')

        l=len(session.get('notifica')[0]['altri'])
        usersL = len(users)

        nome = u['utente'][0]
        return render_template("tok.html",Nmes = l, amici = users, N_amici =usersL -1, nome=nome, check = demo, ragionesociale=u['azienda'])
    
    elif session.get('demo') == True:
        return render_template("tok.html", check=True)
    

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

@app.route("/listaColleghi")
def utenti___superadmin(): 

    def checkRitorno(nome, utenti, ruolo):
        for i in cur.fetchall():
            if i[nome] == u['utente'][0] or i[ruolo] == "superadmin": continue
            else: utenti.append(i)

    if session.get('demo') == "admin" or session.get('demo') == "superadmin":
        u = session.get('utente')
        demo = session.get('demo')

        cur = connPOSTGRES.cursor()

        utenti = []
        if session.get("demo") == "admin":
            cur.execute(f"{Query()['listaColleghi_admin']} WHERE utenti.ragionesociale = '{u['azienda']}'")
            checkRitorno(0,utenti,3)
            
        elif session.get("demo") == "superadmin":
            cur.execute(f"{Query()['listaColleghi_superadmin']}")
            checkRitorno(1, utenti,4)
            
        cur.close()

        try:
            l=len(session.get('notifica')[0]['altri'])
        except: l = 0
        usersL = len(session.get('users'))


    return render_template("Admin/tabelleUtenti.html",
                           Nmes = l, 
                           amici = session.get('users'), 
                           N_amici =usersL -1, 
                           nome=u['utente'][0], 
                           check = demo,
                           links = utenti,
                           ragionesociale=u['azienda']
                           )

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
def report___superadmin(): return render_template("Admin/report.html")

#*************************************************************************************************** ALTRO
#Help
@app.route("/Help", methods=['GET'])
def HELP(): return render_template('componenti/Help.html')  

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
        if session.get("demo") == "superadmin" or session.get("demo") == "admin": 
            risposte.append(modify_DB(elimina, modifica, nome, cognome, email, azienda, cur, connPOSTGRES, check))

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
    except: ...


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
    except: return {"errore": "query non esguita"}

    return jsonify(res)

@app.route('/check/provaAuth')
@requires_auth
def pagina_protetta():
    return render_template("Admin/sql.html")


#*************************************************************************************************** API
@app.route("/registrazione_azienda", methods=['POST'])
def registrazione_azienda_api():
    try:
        return API___azienda(request, connPOSTGRES)
    except Exception as e:
        return str(e), 400

@app.route("/registrazione_utente", methods=['POST'])
def registrazione_utente_api():
    try:
        return API___utente(request, generate_password_hash, connPOSTGRES)
    except Exception as e:
        return str(e), 400

@app.route("/registrazione_documento", methods=['POST'])
def registrazione_documento_api():
    try:
        return API___documento(request)
    except Exception as e:
        return str(e), 400
