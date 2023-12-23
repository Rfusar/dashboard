import string
import random
import string
def slugify_user(nome, cognome, userCode): return f"{nome.lower()}-{cognome.lower()}-{userCode.lower()}"
def slugify_company(nome): 
    slug = ""
    memory = ""
    for lettera in nome:
        if lettera == memory and memory == " ":...
        elif lettera == " ": memory = lettera; slug+="-"
        elif lettera in string.punctuation :...
        else: memory = lettera; slug += lettera.lower()
    if slug[-1] == "-": slug = slug[:-1]
    return slug

ruoli = ['user', 'referent', 'spike-user', 'spike-admin']
businessRuoli = ['ceo', 'coo', 'cfo', 'om', 'pm', 'staff']
#businessRuoliDEFAULT = "staff"
#spike-user = backoffice

def generazione(campo):
    t = ""
    if campo in ["partita IVA", "telefono", "cap"]:
        if campo == "partita IVA": n = 11
        elif campo == "telefono": n = 10
        elif campo == "cap": n = 5

        i = 0
        while i < n: 
            t += random.choice(string.digits)
            i += 1
        return t
    
    elif campo in ["userCode", "str_google", "paperCode", "tag"]: 
        if campo in ["userCode", "paperCode"]: n = 9
        elif campo == "tag": n = 5
        elif campo == "str_google": n = 32

        scelte = string.ascii_letters + string.digits 
        while len(t) < n: t += random.choice(scelte)
        return t

def databaseDEFAULT(DB, COLLECTIONS, dt, password):




    #*azienda
    collection1 = DB[COLLECTIONS[1]]
    collection1.insert_many([
    {
        "staff": [],
        "papers": [],
        "hasDossier": False,
        "active": True,
        "name": "azienda A",
        "vatNum": generazione("partita IVA"),
        "address": {
            "street": "via roma 3",
            "postalCode": generazione('cap'),
            "city": "ornago",
            "state": "MB",
            "country": "italia",
        },
        "contact": {
            "email": "aziA@gmail.com",
            "phone": generazione("telefono"),
        },
        "slug": "azienda-A",
        "seller": None,
        "services":{
            "gdpr":True,
            "rs": False,
            "project": True
        }
    },
    {
        "staff": [],
        "papers": [],
        "hasDossier": True,
        "active": True,
        "name": "azienda B",
        "vatNum": generazione("partita IVA"),
        "address": {
            "street": "via roma 3",
            "postalCode": generazione('cap'),
            "city": "busnago",
            "state": "MB",
            "country": "italia",
        },
        "contact": {
            "email": "aziB@gmail.com",
            "phone": generazione("telefono"),
        },
        "slug": "azienda-B",
        "seller": None,
        "services":{
            "gdpr":True,
            "rs": True,
            "project": False
        }
    },
    {
        "staff": [],
        "papers": [],
        "hasDossier": True,
        "active": True,
        "name": "azienda C",
        "vatNum": generazione("partita IVA"),
        "address": {
            "street": "via vimercate 3",
            "postalCode": generazione("cap"),
            "city": "bellsuco",
            "state": "MB",
            "country": "italia",
        },
        "contact": {
            "email": "aziC@gmail.com",
            "phone": generazione("telefono"),
        },
        "slug": "azienda-C",
        "seller": None,
        "services":{
            "gdpr":True,
            "rs": True,
            "project": False
        }
    }])





    id_A = DB['companies'].find_one({"name": "azienda A"}, {"_id": 1})
    id_B = DB['companies'].find_one({"name": "azienda B"}, {"_id": 1})
    id_C = DB['companies'].find_one({"name": "azienda C"}, {"_id": 1})
    #*users
    collection7 = DB[COLLECTIONS[7]]
    mail = "@gmail.com"
    collection7.insert_many([
    {
        "photo": "photo.png",
        "businessRole": "ceo",
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "riccardo",
            "lastName": "fusaro",
        },
        "contact": {
            "email": f"rfusaro12{mail}",
            "phone": "3452368726"
        },
        "role": "admin",
        "company": id_A["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "riccardo-fusaro",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "John",
            "lastName": "Smith",
        },
        "contact": {
            "email": f"John{mail}",
            "phone": generazione('telefono')
        },
        "role": random.choice(ruoli),
        "company": id_A["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "John-Smith",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Jessy",
            "lastName": "Trust",
        },
        "contact": {
            "email": f"Jessy{mail}",
            "phone": generazione('telefono')
        },
        "role": random.choice(ruoli),
        "company": id_A["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Jessy-Trust",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Anna",
            "lastName": "Jackon",
        },
        "contact": {
            "email": f"Anna{mail}",
            "phone": generazione('telefono')
        },
        "role": random.choice(ruoli),
        "company": id_B["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Anna-Jackon",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Martin",
            "lastName": "Fruc",
        },
        "contact": {
            "email": f"Martin{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_B["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Martin-Fruc",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Jimmy",
            "lastName": "Druck",
        },
        "contact": {
            "email": f"Jimmy{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_B["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Jimmy-Druck",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Tonia",
            "lastName": "Tessex",
        },
        "contact": {
            "email": f"Tonia{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_C["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Tonia-Tessex",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Francesco",
            "lastName": "Xanos",
        },
        "contact": {
            "email": f"Francesco{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_C["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Francesco-Xanos",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Cloey",
            "lastName": "Jason",
        },
        "contact": {
            "email": f"Cloey{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_C["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Cloey-Jason",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },
    {
        "photo": "photo.png",
        "businessRole": random.choice(businessRuoli),
        "active": True,
        "validated": True,
        "createAt": dt.now(),
        "name": {
            "firstName": "Aziz",
            "lastName": "khalifa",
        },
        "contact": {
            "email": f"Aziz{mail}",
            "phone": generazione("telefono")
        },
        "role": random.choice(ruoli),
        "company": id_B["_id"],
        "password": password,
        "userCode": generazione("userCode"),
        "slug": "Aziz-khalifa",
        "passwordChange": dt.now(),
        "updateAt": dt.now()
    },

    ])

    #fase caricamento staff a company
    id_users___A = DB['users'].find({"company": id_A}, {"_id": 1})
    id_users___B = DB['users'].find({"company": id_B}, {"_id": 1})
    id_users___C = DB['users'].find({"company": id_C}, {"_id": 1})
    for id in id_users___A: DB['companies'].update_one({"company": id_A}, {"$push":{"staff":id["_id"]}})   
    for id in id_users___B: DB['companies'].update_one({"company": id_B}, {"$push":{"staff":id["_id"]}})
    for id in id_users___C: DB['companies'].update_one({"company": id_C}, {"$push":{"staff":id["_id"]}})


    ID_per = DB['users'].find_one({"name.firstName": "Aziz"}, {"_id": 1})
    #*ticktes
    collection6 = DB[COLLECTIONS[6]]
    collection6.insert_one({
        "status": "active",
        "urgency": False,
        "assigned": True,
        "assignedTO": ID_per["_id"],
        "title": "toket1",
        "description": "servizio attivo??",
        "company": id_C["_id"],
        "person": ID_per["_id"],
        "ticketCode": generazione("userCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "sdfs-dfsdfsd-fsdf"
    })


    ID_tic = DB['tickets'].find_one({"status": "active"}, {'_id': 1})
    #*comments
    collection0 = DB[COLLECTIONS[0]]
    collection0.insert_many([
    {
        "ticket": ID_tic['_id'],
        "author": ID_per["_id"],
        "comment": "buongiorno, mi servirebbe il resoconto dell'anno 2022",
        "createAt": dt.now()
    },
    {
        "ticket": ID_tic['_id'],
        "author": ID_per["_id"],
        "comment": "buongiorno, mi servirebbe il resoconto dell'anno 2022",
        "createAt": dt.now()
    },
    ])

    
    #*dossier
    collection2 = DB[COLLECTIONS[2]]
    collection2.insert_many([
    {
        "company": id_A["_id"],
        "year": 2023,
        "category": "gdpr",
        "createAt": dt.now(),
        "updateAT": dt.now(),
    },
    {
        "company": id_B["_id"],
        "year": 2023,
        "category": "gdpr",
        "createAt": dt.now(),
        "updateAT": dt.now(),
    },
    {
        "company": id_C["_id"],
        "year": 2023,
        "category": "gdpr",
        "createAt": dt.now(),
        "updateAT": dt.now(),
    },
    {
        "company": id_B["_id"],
        "year": 2022,
        "category": "gdpr",
        "createAt": dt.now(),
        "updateAT": dt.now(),
    },
    {
        "company": id_C["_id"],
        "year": 2022,
        "category": "gdpr",
        "createAt": dt.now(),
        "updateAT": dt.now(),
    }
    ])



    #*paper
    collection3 = DB[COLLECTIONS[3]]
    collection3.insert_many([
    {
        "title": "foglio1",
        "description": "descrizione",
        "company": id_A["_id"],
        "category": "gdpr",
        "tags": generazione("tag"),
        "file": f"{generazione('str_google')}.pdf",
        "paperCode": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-as-dd",
        "yearValidation": 2023
    },
    {
        "title": "foglio2",
        "description": "descrizione",
        "company": id_A["_id"],
        "category": "gdpr",
        "tags": generazione("tag"),
        "file": f"{generazione('str_google')}.pdf",
        "paperCode": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-a-dd",
        "yearValidation": 2023
    },
    {
        "title": "foglio3",
        "description": "descrizione",
        "company": id_C["_id"],
        "category": "gdpr",
        "tags": generazione("tag"),
        "file": f"{generazione('str_google')}.pdf",
        "paperCode": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-wer-reee",
        "yearValidation": 2023
    },
    {
        "title": "foglio4",
        "description": "descrizione",
        "company": id_B["_id"],
        "category": "gdpr",
        "tags": generazione("tag"),
        "file": f"{generazione('str_google')}.pdf",
        "paperCode": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-as-qqq",
        "yearValidation": 2023
    },
    {
        "title": "foglio5",
        "description": "descrizione",
        "company": id_B["_id"],
        "category": "gdpr",
        "tags": generazione("tag"),
        "file": f"{generazione('str_google')}.pdf",
        "paperCode": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-as-zzazaz",
        "yearValidation": 2023
    }
    
    ])

    #*project
    collection5 = DB[COLLECTIONS[5]]
    collection5.insert_one({
        "author": ID_per["_id"],
        "authorizedRoles": ["user", "admin"],
        "title": "project",
        "description": "progetto di prova",
        "company": id_B["_id"],
        "status": "attivo",
        "code": generazione("paperCode"),
        "slug": "asdas-try-lj",
        "createAt": dt.now(),
        "updateAT": dt.now()
    })
    ID_pro = DB['projects'].find_one({"title": "project"},{"_id": 1})
    #*projectFiles
    collection4 = DB[COLLECTIONS[4]]
    collection4.insert_one({
        "title": "progetto 1",
        "description": "prova",
        "company": id_B["_id"],
        "project": ID_pro['_id'],
        "file": "nomeFile",
        "code": generazione("paperCode"),
        "createAt": dt.now(),
        "updateAT": dt.now(),
        "slug": "asd-asdasd-sad"
    })

    


