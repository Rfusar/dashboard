from .DB import DB, client
def listaColleghi(email) -> list[dict]:
    class User:
        def __init__(self, ID, ragionesociale, nome, cognome, email, phone, ruolo, businessRole, active, validated):
            self.ID = ID
            self.ragionesociale = ragionesociale
            self.nome = nome
            self.cognome = cognome
            self.email = email
            self.phone = phone
            self.ruolo = ruolo
            self.businessRole = businessRole
            self.active = active
            self.validated = validated

        def utente(self, array):
            ruoli = {
                "base": self.ruolo,
                "business":self.businessRole
            }
            persona = {
                "idetificazione": {
                    "nome": self.nome, 
                    "cognome": self.cognome, 
                    "nome_cognome": f"{self.nome} {self.cognome}"
                },
                "contatti":{
                    "email": self.email,
                    "phone": self.phone
                }
            }
            ogg = {"ID": self.ID, "azienda": self.ragionesociale, "utente": persona, "ruoli": ruoli, "active": self.active, "validate": self.validated}
            array.append(ogg)

    UTENTE = DB['users'].find_one({"contact.email": email})

    common_projection = {
        "_id": 1,
        "company": 1, 
        "name.firstName": 1, 
        "name.lastName": 1, 
        "contact.email": 1, 
        "contact.phone": 1, 
        "role": 1,
        "businessRole": 1,
        "active": 1,
        "validated": 1, 
    }

    if UTENTE['role'] == "admin":
        users = DB['users'].find({}, common_projection)

    elif UTENTE['role'] == "spike-admin":
        users = DB['users'].find({"company": UTENTE['company']}, common_projection)

    elif UTENTE['role'] == "spike-user":
        users = DB['users'].find({"company": UTENTE['company'], "role": {"$in": ["user", "spike-user"]}}, common_projection)

    USER = [] 
    for i in users: User(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]).utente(USER) 
    client.close() 

    return USER





