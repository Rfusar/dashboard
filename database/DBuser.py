from .DB import connPOSTGRES

def listaColleghi(RG) -> list[dict]:

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
    cur.execute('SELECT nome, livello FROM ruoli WHERE ragionesociale = %s', (RG,))
    r = cur.fetchall()

    USER = [] 
    for i in u: 
        for j in r:
            if j[0] == i[0]:
                User(i[0], i[1], i[2], i[3], j[1]).utente(USER); break
            
    cur.close() 
    return USER
'''
def ruoloUtente(nome) -> dict:
    class Admin:
        def __init__(self, nome):
            self.nome = nome

        def creatore(self): ogg={"superadmin": self.nome}; return ogg
        def amministratore(self): ogg={"admin": self.nome}; return ogg
        def utente(self): ogg={"utente": self.nome}; return ogg

    cur = connPOSTGRES.cursor()

    cur.execute('SELECT livello FROM ruoli WHERE nome = %s',(nome,))
    u = cur.fetchall()
    
    if u[0][0] == "superadmin": return Admin(nome).creatore()
    elif u[0][0] == "admin": return Admin(nome).amministratore()
    elif u[0][0] == "utente": return Admin(nome).utente()
'''




