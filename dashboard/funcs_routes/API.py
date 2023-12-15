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
    try:
        cur = connPOSTGRES.cursor()
        cur.execute("INSERT INTO azienda (ragionesociale, partitaiva, indirizzo, comune, provincia, cap, nazione, email, pec, tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                        (Ragionesociale, Partitaiva, Indirizzo, Comune, Provincia, Cap, Nazione, Email, Pec, Telefono))
        connPOSTGRES.commit()
        cur.close()
        return "registrazione completata", 200
    
    except Exception as e: return str(e), 400

