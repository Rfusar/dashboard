from .DB import DB, client
def listaColleghi(email) -> list[dict]:
    class User:
        def __init__(self, ID, ragionesocialeID, ragionesociale, nome, cognome, email, phone, ruolo, businessRole, active, validated):
            self.ID = ID
            self.ragionesocialeID = ragionesocialeID
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
                "identificazione": {
                    "nome": self.nome, 
                    "cognome": self.cognome, 
                    "nome_cognome": f"{self.nome} {self.cognome}"
                },
                "contatti":{
                    "email": self.email,
                    "phone": self.phone
                }
            }
            descrizioneAzienda = {
                "ID": self.ragionesocialeID,
                "nome": self.ragionesociale,
            }
            ogg = {"ID": self.ID, "azienda": descrizioneAzienda, "utente": persona, "ruoli": ruoli, "active": self.active, "validate": self.validated}
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

    if UTENTE['role'] == "spike-admin":
        users = DB['users'].find({}, common_projection)

    elif UTENTE['role'] == "spike-user":
        users = DB['users'].find({"company": UTENTE['company'], "role": {"$in": ['spike-user']}}, common_projection)

    elif UTENTE['role'] == "referente":
        users = DB['users'].find({"company": UTENTE['company'], "role": {"$in": ['user', 'referent']}}, common_projection)

    elif UTENTE['role'] == "user":
        users = DB['users'].find({"company": UTENTE['company'], "role": {"$in": ["user", "spike-user"]}}, common_projection)


    USER = [] 
    for i in users: 
        nome_azienda = DB['companies'].find_one({"_id": i['company']}, {"name": 1})
        User(str(i['_id']), str(i['company']), nome_azienda['name'], i["name"]['firstName'], i["name"]['lastName'], i['contact']["email"], 
                         i["contact"]["phone"], i["role"], i["businessRole"], i["active"], i["validated"]).utente(USER) 


    return USER





