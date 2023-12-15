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
    cur.execute('SELECT nome, cognome, ragionesociale, email FROM utenti WHERE ragionesociale = %s',(RG,))
    u = cur.fetchall()
    cur.execute('SELECT email, livello FROM ruoli WHERE ragionesociale = %s', (RG,))
    r = cur.fetchall()



    USER = [] 
    for i in u: 
        for j in r:
            if j[3] == i[0]:
                User(i[0], i[1], i[2], i[3], j[1]).utente(USER); break
            
    cur.close() 
    return USER





