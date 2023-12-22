from dashboard import app
from flask import render_template,jsonify,request,session, redirect, url_for
import bcrypt
from database.DB import DB
from database.DBchat import chat, readChat,notifica, readNotifica, allNotifica
from database.DBuser import listaColleghi
from functools import wraps
#from .classDefinition import RegistrazioneForm,LoginForm
from datetime import datetime as dt
#funzioni_per_semplificare
from dashboard.funcs_routes.funcs1 import checkMese, Documenti__da_DB, Query, modify_DB, Token
from dashboard.funcs_routes.Utenza import LOGIN, REGISTER, reset_password
from dashboard.funcs_routes.Pagine_principali import principale___utente, principale___admin, principale__superadmin
from dashboard.funcs_routes.API import API___azienda, API___utente, API___documento, FUNCS_API


#*START
@app.route("/")
def home():
    session['demo'] = True
    return render_template('index.html', check = True, title= "Repository_GDPR")
    

#*************************************************************************************************** UTENZA
#-----> registrazione
@app.route("/registrazione")#PAGINA
def registrazione(): return render_template("user/register.html")
@app.route("/fetchRegister", methods=["POST"])#FUNZIONE
def logicaRegistrazione(): return REGISTER(request, bcrypt, DB, redirect, url_for, dt, Token)
#-----> login 
@app.route("/login")#PAGINA
def login(): return render_template("user/login.html")
@app.route("/fetchUtente", methods=["POST"])#FUNZIONE
def logicaLogin(): return LOGIN(request, DB, listaColleghi, session, bcrypt, redirect, url_for)        
#-----> resetPassword
@app.route("/resetPassword")#PAGINA
def resetPassword(): return render_template("user/forgot-password.html")
@app.route("/fetchResetPassword", methods=["POST"])#FUNZIONE
def logicaResetPassword(): return reset_password(request, bcrypt, DB, redirect, url_for)
  
#LOGOUT
@app.route('/logout')
def logout():
    session['utente'] = None
    session['users'] = None
    session['messaggi'] = None
    session['demo'] = True
    return redirect(url_for('home'))


#*************************************************************************************************** Principale
@app.route("/HOME")
def HOME():
    if session.get('demo') == "spike-user":
        return principale___utente(session, readChat, allNotifica, readNotifica, dt, render_template, checkMese, DB)
    
    elif session.get('demo') == "spike-admin":
        return principale___admin(session, render_template, dt, checkMese)
    
    elif session.get('demo') == "admin":
        return principale__superadmin(session, render_template, dt, checkMese)
    
    else:
        return render_template("informazioni/404.html")

#PAGINE
@app.route("/charts")
def charts():
    if session.get('demo') == "utente" or session.get('demo') == "admin" or session.get('demo') == "superadmin":
        u = session.get('utente')

        try: 
            l=len(session['notifica'][0]['altri'])
        except: l = 0
        usersL = len(session.get('users'))
        
        return render_template("charts.html",
                               Nmes = l, 
                               amici = session.get('users'), 
                               N_amici =usersL -1, 
                               nome=u['utente'][0], 
                               check = session.get('demo'), 
                               ruolo = session.get("demo"), 
                               ragionesociale=u['azienda'])
    

    
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
    '''
    cur = connPOSTGRES.cursor()
    DOCUMENTI_MUTUI = Documenti__da_DB(cur, session, "MUTUI")
    DATI['documenti_mutuo'] = DOCUMENTI_MUTUI
    cur.close()
    '''

    return jsonify(DATI)

@app.route("/table")
def table():
    if session.get('demo') in ["utente", "admin","superadmin"]:
        u = session.get('utente')

        try:
            l=len(session['notifica'][0]['altri'])
        except: l = 0
        usersL = len(session.get('users'))


        return render_template("tables.html",
                               Nmes = l, 
                               amici = session.get('users'), 
                               N_amici =usersL -1, 
                               links = [], 
                               nome = u['utente'][0], 
                               check= session.get('demo'), 
                               ruolo = session.get("demo"), 
                               ragionesociale=u['azienda'])

    elif session.get('demo') == True:
            return render_template("tables.html", check=True)

#---------> MESSAGGI
#CHAT
@app.route("/chat/<a>/<b>/<c>/<d>/<e>", methods=['GET'])
def a(a,b,c,d,e): chat(a,b,c,d,e)

#NOTIFICA
@app.route("/notifica/<a>/<b>/<c>/<d>", methods=['GET'])
def b(a,b,c,d):
    if session.get("demo") == "utente" or session.get("demo") == "admin":
        azienda = session.get("utente")['azienda']
        notifica(a,b,c,d,azienda)
        
    elif session.get("demo") == "superadmin":
        for A in DB['companies'].find({}, {"name":1}):
            notifica(a,b,c,d,A)

@app.route("/modifica/<nome>")
def modifica_utente(nome):
    u = session.get('utente')

    try:
        l=len(session['notifica'][0]['altri'])
    except: l = 0
    usersL = len(session.get('users'))
    

    return render_template("/modifica_utente.html",
                           Nmes = l, 
                           amici = session.get('users'), 
                           N_amici =usersL -1, 
                           links = [], 
                           nome = u['utente'][0], 
                           check= session.get('demo'), 
                           ruolo = session.get("demo"), 
                           ragionesociale=u['azienda'])



#*************************************************************************************************** Pagine AMMINISTRATORI
@app.route("/adminCheck")
def adminCheck():
    if session.get('demo') == "admin":
        nomeAzienda = session.get('utente')['azienda']

        #CHECK CHAT
        nomiUSERS = DB['users'].find({'company': nomeAzienda},{'name.firstName': 1})

        try:
            CHAT = {}
            for i in range(0, len(nomiUSERS)):
                if  i == len(nomiUSERS)-1: 
                    CHAT['chat'] = readChat(nomiUSERS[0][0], nomiUSERS[i][0])
                CHAT['chat'] = readChat(nomiUSERS[i+1][0], nomiUSERS[i][0])
        except:...

        result ={
            'utenti':nomiUSERS,
            'chat':CHAT,
           }
        return jsonify(result)
    
    else: return {"mess": "non puoi"}

@app.route("/superadminCheck")
def superadminCheck():
    if session.get('demo') == "superadmin":
        #CHECK CHAT
        users = session.get('users')
        nomiUSERS = []
        for U in users : nomiUSERS.append(U['utente'][0])

        try:
            CHAT = {}
            for i in range(len(nomiUSERS)):
                if  i == len(nomiUSERS)-1: 
                    CHAT['chat'] = readChat(nomiUSERS[0][0], nomiUSERS[i][0])
                CHAT['chat'] = readChat(nomiUSERS[i+1][0], nomiUSERS[i][0])
        except:...

        aziende = list(DB['companies'].find())
        result = { 'utenti': users, 'chat':CHAT, 'aziende': aziende }
        
        return jsonify(result)
    
    else: return {"mess": "non puoi"}

#--------> CHECK UTENTI
@app.route("/listaColleghi")
def utenti___superadmin(): 
    if session.get('demo') in ["admin", "superadmin"]:
        u = session.get('utente')


        if session.get("demo") == "admin":
            utenti = DB['users'].find({'company': u['azienda']})
            
            
        elif session.get("demo") == "superadmin":
            utenti = DB['users'].find()

        try:
            l=len(session.get('notifica')[0]['altri'])
        except: l = 0
        usersL = len(session.get('users'))


    return render_template("Admin/tabelleUtenti.html",
                           Nmes = l, 
                           amici = session.get('users'), 
                           N_amici =usersL -1, 
                           nome=u['utente'][0], 
                           check = session.get('demo'),
                           links = utenti,
                           ruolo = session.get("demo"), 
                           ragionesociale=u['azienda']
                           )

@app.route("/Tickets")
def Tickets():
    u = session.get('utente')

    try:
        l=len(session['notifica'][0]['altri'])
    except: l = 0
    usersL = len(session.get('users'))

    return render_template("/tickets.html",
                           Nmes = l, 
                           amici = session.get('users'), 
                           N_amici =usersL -1, 
                           links = [], 
                           nome = u['utente'][0], 
                           check= session.get('demo'), 
                           ruolo = session.get("demo"), 
                           ragionesociale=u['azienda'])

@app.route("/superadmin/aziende")
def aziende___superadmin(): 
    if session.get('demo') == "superadmin":
        u = session.get('utente')

        aziende = DB['companies'].find()

        try:
            l = len(session.get('notifica')[0]['altri'])
        except:l = 0
        usersL = len(session.get('users'))

        return render_template("Admin/tabelleAziende.html", 
                                Nmes = l, 
                                amici = session.get('users'), 
                                N_amici =usersL -1, 
                                nome=u['utente'][0],
                                check = session.get('demo'),
                                links = aziende,
                                ruolo = session.get("demo"), 
                                ragionesociale=u['azienda']
                                )

@app.route("/superadmin/checkAziende", methods=["POST"])
def check_aziende___superadmin():
    if session.get('demo') == "superadmin":
        aziende = DB['companies'].find()
        return jsonify(aziende)

@app.route("/superadmin/report")
def report___superadmin(): return render_template("Admin/report.html")


#*************************************************************************************************** ALTRO
#Dettagli
@app.route("/utente/<ID>", methods=["GET"])
def area_utente(ID):
    if session.get("demo") in ["admin", "superadmin"]:

        U = DB['users'].find_one({"_id":ID})
        user = DB['users'].find({'email': U['email']})
        azienda = DB['companies'].find_one({"name": U['company']})

        tiks = [["sadas","blalbab","attivo","gigino","22/03/2023"],
                ["sadas","blalbab","non attivo","---","23/12/2023"],
                ["sadas","blalbab","attivo","gigino","22/03/2022"],
                ["sadas","blalbab","attivo","gigino","22/03/2022"],
                ["sadas","blalbab","non attivo","---","22/03/2022"]]
        
        return render_template("area_utente.html", 
                                   check= session.get('demo'),
                                   nome= session.get('utente')['utente'][0],
                                   ragionesociale= session.get('utente')['azienda'],
                                   user = user,
                                   azienda = azienda,
                                   ruolo = session.get("demo"), 
                                   tiks = tiks
                                  )
    
@app.route("/azienda/<ID>", methods=["GET"])
def area_azienda(ID):
    if session.get("demo") in ["admin", "superadmin"]:

        datiAzienda = DB['companies'].find({"_id":ID})
        datiUser = DB['users'].find({'company': datiAzienda['name']}, {"name.lastName": 1,})

        docs = [["sadas","titoli1","22/03/2022"], ["sadas","titoli1","22/03/2022"], ["sadas","titoli1","22/03/2022"]]
        tiks = [["sadas","attivo","22/03/2022"],["sadas","non attivo","22/03/2022"],["sadas","attivo","22/03/2022"]]
        
        return render_template("area_azienda.html", 
                                   check=session.get('demo'),
                                   nome= session.get('utente')['utente'][0],
                                   ragionesociale= session.get('utente')['azienda'],
                                   azienda = datiAzienda,
                                   user = datiUser,
                                   docs = docs,
                                   ruolo = session.get("demo"), 
                                   tiks = tiks
                                  )



#Help
@app.route("/Help")
def HELP(): return render_template('componenti/Help.html')  
'''
@app.route("/modificaDB", methods=['POST'])
def modificaDB():
    if session.get("demo") in ["admin", "superadmin"]:
        utente = request.json

        cur = connPOSTGRES.cursor()
        risposta = modify_DB(utente, cur, connPOSTGRES)
        cur.close()
    
        return jsonify(risposta)
'''



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
'''
#capacita d'interagire con DB
def requires_auth(f):
    def check_credentials(username, password): return username == "admintech" and password == "123456"
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
def pagina_protetta(): return render_template("Admin/sql.html")
'''

#*************************************************************************************************** API
@app.route("/registrazione_azienda", methods=['POST'])
def registrazione_azienda_api(): return FUNCS_API(API___azienda, request, DB, None, 0)

@app.route("/registrazione_utente", methods=['POST'])
def registrazione_utente_api(): return FUNCS_API(API___utente, request, DB, bcrypt, 1)

@app.route("/registrazione_documento", methods=['POST'])
def registrazione_documento_api(): return FUNCS_API(API___documento, request, None, None, 2)

'''
COSE DA FARE:
    - Gestione tickets
    - Query Documenti (voce: file)
        --rilascio link?

'''