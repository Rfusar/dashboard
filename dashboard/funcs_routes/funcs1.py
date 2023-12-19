
def checkMese(dt):
    ANNO = ["Gennaio", "Febbraio" "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    for n in range(len(ANNO)+1): 
        if dt.now().month == n+1: 
            return ANNO[n-1]

def Documenti__da_DB(cur, session, check):
    Prompt = ["""
              SELECT 
                documento->>'doctype',
                documento->>'creditinstitute',
                documento->>'borrower',
                documento->>'borrowerfiscalcode',
                documento->>'emissiondate',
                documento->>'amount',
                documento->>'duration',
                documento->>'taxtype',
                documento->>'ipoteca',
                documento->>'typeipoteca',
                documento->>'fideiussione',
                documento->>'fideiussore',
                documento->>'numberbuilding',
                documento->>'addressbuilding',
                documento->>'category',
                documento->>'paper',
                documento->>'particel',
                documento->>'map'
            FROM documenti
              """]
    
    if check == "MUTUI":
        cur.execute(f"{Prompt[0]} WHERE ragionesociale = '{session.get('utente')['azienda']}'")
        return cur.fetchall()
    
def Query():
    a = """SELECT 
            utenti.ragionesociale,
            utenti.nome, 
            utenti.cognome, 
            utenti.email, 
            ruoli.livello 
        FROM utenti 
        JOIN ruoli 
        ON utenti.email = ruoli.email"""
    
    b= """SELECT 
            utenti.nome, 
            utenti.cognome, 
            utenti.email, 
            ruoli.livello 
        FROM utenti 
        JOIN ruoli 
        ON utenti.email = ruoli.email"""
    
    c = """SELECT 
            utenti.nome,
            utenti.cognome, 
            utenti.email, 
            utenti.tel, 
            ruoli.livello 
        FROM utenti 
        JOIN ruoli 
        ON utenti.email = ruoli.email"""
    
    d = """SELECT
            azienda.ragionesociale,
            azienda.partitaiva,
            azienda.cap,
            azienda.nazione,
            azienda.pec
        FROM azienda
        JOIN utenti
        ON azienda.ragionesociale = utenti.ragionesociale
"""
    
    #OGGETTO
    ogg={
        "listaColleghi_superadmin": a,
        "listaColleghi_admin": b,
        "area_utenti1": c,
        "area_utenti2": d,
        }
    
    return ogg


def modify_DB(utente, cur, connPOSTGRES):
    email = utente.get('email')
    modifica = utente.get('modifica')
    elimina = utente.get('elimina')

    check = ""
    if elimina:
            cur.execute(f"DELETE FROM ruoli WHERE email = '{email}'")
            connPOSTGRES.commit()
            cur.execute(f"DELETE FROM utenti WHERE email = '{email}'")
            connPOSTGRES.commit()
            check += "eliminato"

    elif  modifica:
        cur.execute(f"UPDATE ruoli SET livello = 'admin' WHERE email = '{email}'")
        connPOSTGRES.commit()
        check += "reso admin"

    return f"L'utente {email}; {check} con successo"
    
    




    
