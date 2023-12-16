
def checkMese(dt):
    ANNO = ["Gennaio", "Febbraio" "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    for n in range(len(ANNO)+1): 
        if dt.now().month == n+1: return ANNO[n-1]



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
        cur.execute(f"{Prompt[0]} WHERE ragionesociale = %s ", (session.get('utente')['azienda'],))
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
        ON utenti.nome = ruoli.nome"""
    
    b= """SELECT 
            utenti.nome, 
            utenti.cognome, 
            utenti.email, 
            ruoli.livello 
        FROM utenti 
        JOIN ruoli 
        ON utenti.nome = ruoli.nome"""
    
    #OGGETTO
    ogg={
        "listaColleghi_superadmin": a,
        "listaColleghi_admin": b
        }
    
    return ogg


def modify_DB(elimina, modifica, nome, cognome, email, azienda, cur, connPOSTGRES, check):
    if elimina:
            cur.execute(f"DELETE FROM ruoli WHERE nome = '{nome}' and ragionesociale = '{azienda}'")
            connPOSTGRES.commit()
            cur.execute(f"DELETE FROM utenti WHERE nome = '{nome}' and cognome = '{cognome}' and email = '{email}' and ragionesociale = '{azienda}'")
            connPOSTGRES.commit()
            check += "eliminato"

    elif  modifica:
        cur.execute(f"UPDATE ruoli SET livello = 'admin' WHERE nome = '{nome}'")
        connPOSTGRES.commit()
        check += "reso admin"

    return f"L'utente {nome} {cognome}, lavora presso: {azienda}; {check} con successo"


    
