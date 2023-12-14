
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
    




    
