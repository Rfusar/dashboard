def API___azienda(request, connPOSTGRES):
    data =  request.get_json()
    Ragionesociale = data.get('Ragionesociale')
    Partitaiva = data.get('Partitaiva')
    Indirizzo = data.get('Indirizzo')
    Comune = data.get('Comune')
    Provincia = data.get('Provincia')
    Cap = data.get('Cap')
    Nazione = data.get('Nazione')
    Email = data.get('Email')
    Pec = data.get('Pec')
    Telefono = data.get('Tel')

    cur = connPOSTGRES.cursor()
    cur.execute("INSERT INTO azienda (ragionesociale, partitaiva, indirizzo, comune, provincia, cap, nazione, email, pec, tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (Ragionesociale, Partitaiva, Indirizzo, Comune, Provincia, Cap, Nazione, Email, Pec, Telefono))
    connPOSTGRES.commit()
    cur.close()

    return "registrazione completata", 200

def API___utente(request, generate_password_hash, connPOSTGRES):
    data = request.get_json()
    nome = data.get('Nome')
    cognome = data.get('Cognome')
    telefono = data.get('Telefono')
    RG = data.get('Ragionesociale')
    email = data.get('Email')
    password = data.get('Password')
    ruolo = data.get('Ruolo')

    p = generate_password_hash(password)

    try:    
        cur = connPOSTGRES.cursor()
        cur.execute("insert into utenti (nome, cognome, tel, ragionesociale, email, password) values (%s,%s,%s,%s,%s,%s)",(nome, cognome, telefono, RG, email, p))
        connPOSTGRES.commit()
        cur.execute("insert into ruoli (email, ragionesociale, livello) values (%s,%s,%s)", (email, RG, ruolo))
        connPOSTGRES.commit()
        cur.close()
        return "registrazione completata", 200
    
    except Exception as e:
            return str(e), 400

def API___documento(request):
    data = request.get_json()
    id = data.get("Id")
    TITOLO = data.get("Nome_file")
    USER_GPT = data.get('User')
    SYSTEM_GPT = data.get("System")
    Ragionesociale = data.get("Ragionesociale")

    with open(f"C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\gestioneErrori\\{TITOLO}.txt", "w", encoding="utf-8") as f:
        f.write(f"{id}\n\n{USER_GPT}\n\n\n{SYSTEM_GPT}\n\n{Ragionesociale}")

    '''
    try: 
        risposta = interact_with_chatgpt_prova(USER_GPT, SYSTEM_GPT, api_key, maxContent, creativita)
        cur = connPOSTGRES.cursor()
        cur.execute('INSERT INTO documenti (documento, token, nome_file, ragionesociale) VALUES (%s,%s,%s)',(risposta[0], risposta[1], TITOLO, Ragionesociale))
        connPOSTGRES.commit()
        cur.close()

    except Exception as e:
        return str(e), 400
    '''

    return "registrazione completata", 200

#GESTIONE -> funcs API
def FUNCS_API(func, request, connPOSTGRES, generate_password_hash, API):
    try:
        if API == 0: return func(request, connPOSTGRES)
        elif API == 1: return func(request, generate_password_hash, connPOSTGRES)
        elif API == 2: return func(request)
    except Exception as e:
        return str(e)