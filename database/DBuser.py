from .DB import connPOSTGRES

def listaColleghi(RG, email) -> list[dict]:

    class User:
        def __init__(self, nome, cognome, ragionesociale, email, ruolo):
            self.nome = nome
            self.cognome = cognome
            self.ragionesociale = ragionesociale
            self.email = email
            self.ruolo = ruolo

        def utente(self, array):
            nome_e_cognome = [self.nome, self.cognome, f"{self.nome} {self.cognome}"]

            ogg = {"azienda": self.ragionesociale, "utente": nome_e_cognome, "email": self.email, "ruolo": self.ruolo}
            array.append(ogg)

    cur = connPOSTGRES.cursor()
    cur.execute("SELECT email, livello FROM ruoli")

    for i in cur.fetchall():
        if email == i[0]: UTENTE = i

    query = """SELECT 
                    utenti.nome, 
                    utenti.cognome, 
                    utenti.ragionesociale, 
                    utenti.email,
                    ruoli.livello 
                FROM utenti 
                JOIN ruoli 
                ON utenti.email = ruoli.email"""

    if UTENTE[1] == "superadmin": cur.execute(f"{query}")

    elif UTENTE[1] == "admin": cur.execute(f"{query} WHERE utenti.ragionesociale = '{RG}' and (ruoli.livello = 'utente' or ruoli.livello = 'admin')")

    elif UTENTE[1] == "utente": cur.execute(f"{query} WHERE utenti.ragionesociale = '{RG}' and ruoli.livello = 'utente'")

    USER = [] 
    for i in cur.fetchall(): User(i[0], i[1], i[2], i[3], i[4]).utente(USER) 
    cur.close() 

    return USER





