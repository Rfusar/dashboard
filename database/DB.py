#CLUSTER_PROD = os.getenv("CLUSTER_PROD")
#PASSWORD_PROD = os.getenv("PASSWORD_PROD")
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime as dt
#from databasePROVA import databaseDEFAULT
#from pprint import pprint as ppr
load_dotenv("C:\\Users\\Utente\\Desktop\\info\\variabili\\.env")


UTENTE = os.getenv("UTENTE")

CLUSTER_DEV = os.getenv("CLUSTER_DEV")
PASSWORD_DEV = os.getenv("PASSWORD_DEV")


DATABASE = ["spike", "test"]
COLLECTIONS = ["comments", "companies", "dossiers", "projectfiles", "paper", "projects", "tickets", "users"]


client = MongoClient(f"mongodb+srv://{UTENTE}:{PASSWORD_DEV}@{CLUSTER_DEV}.mongodb.net/")
DB = client[DATABASE[1]]





'''
for collection in COLLECTIONS: 
    DB[collection].delete_many({})

password0 = "CHIOCCIOLA13$$$"
password = bcrypt.hashpw(password0.encode('utf-8'), bcrypt.gensalt(12))

databaseDEFAULT(DB, COLLECTIONS, dt, password)

'''






'''
#*commenti
collection0 = DB[COLLECTIONS[0]]
collection0.insert_one({
    "ticket": "eidfsoidf87d6sadkjas",
    "author": "sjdhfsdf87ds6fdshfsf",
    "comment": "buongiorno, mi servirebbe il resoconto dell'anno 2022",
    "createAt": "22/04/2023 12:03:45"
})

#*azienda
collection1 = DB[COLLECTIONS[1]]
collection1.insert_one({
    "staff": [],
    "papers": [],
    "hasDossier": False,
    "active": True,
    "name": "azienda A",
    "vatNum": "12354231425",
    "address": {
        "street": "via roma 3",
        "postalCode": "67348",
        "city": "ornago",
        "state": "MB",
        "country": "italia",
    },
    "contact": {
        "email": "azie@gmail.com",
        "phone": "3456781234",
    },
    "slug": "azienda-A",
    "seller": "adskjfsfsaiudfads7fsafy",
    "services":{
        "gdpr":True
    }
})

#*dossier
collection2 = DB[COLLECTIONS[2]]
collection2.insert_one({
    "company": "isajdfoiadsfas7d6fasf",
    "year": 2023,
    "category": "gdpr",
    "createAt": "22/04/2023 12:03:45",
    "updateAT": "22/04/2023 12:03:45",
})
#*paper
collection3 = DB[COLLECTIONS[3]]
collection3.insert_one({
    "title": "foglio1",
    "description": "descrizione",
    "company": "asdasdasd7asda87sdw",
    "category": "gdpr",
    "tags": "asdsad",
    "file": "stringa-goolge",
    "paperCode": "stdferfih",
    "createAt": "22/04/2023 12:03:45",
    "updateAT": "22/04/2023 12:03:45",
    "slug": "asd-asd-ss",
    "yearValidation": 2023
})

#*projectFiles
collection4 = DB[COLLECTIONS[4]]
collection4.insert_one({
    "title": "progetto 1",
    "description": "prova",
    "company": "jdsahsafs87dfsd87f",
    "project": "kjdsfkjdsf8sdfs8dfds7f",
    "file": "nomeFile",
    "code": "trshikopd",
    "createAt": "22/04/2023 12:03:45",
    "updateAT": "22/04/2023 12:03:45",
    "slug": "asd-asdasd-sad"
})

#*project
collection5 = DB[COLLECTIONS[5]]
collection5.insert_one({
    "author": "sadasdasdsa7da7sdaa",
    "authorizedRoles": ["user", "admin"],
    "title": "project",
    "description": "progetto di prova",
    "company": "asjdhasdsadas6da6sa6",
    "status": "attivo",
    "code": "jsugdtcvr",
    "slug": "asdas-try-lj",
    "createAt": "22/04/2023 12:03:45",
    "updateAT": "22/04/2023 12:03:45"
})
#*ticktes
collection6 = DB[COLLECTIONS[6]]
collection6.insert_one({
    "status": "acttive",
    "urgency": False,
    "assigned": True,
    "assignedTO": "sdfdsf7sdf7dsf6sdfsd",
    "title": "toket1",
    "description": "serzio attivo??",
    "company": "afadsf8saf7asdfdajfdfh",
    "person": "iusdfsd6afddsf6adsfjs",
    "ticketCode": "aokstdfrw",
    "createAt": "22/04/2023 12:03:45",
    "updateAT": "22/04/2023 12:03:45",
    "slug": "sdfs-dfsdfsd-fsdf"
})

#*users
collection7 = DB[COLLECTIONS[7]]
collection7.insert_one({
    "photo": "photo.png",
    "businessRole": "ceo",
    "active": True,
    "validated": True,
    "createAt": "23/10/2023 12:50:23",
    "name": {
        "firstName": "riccardo",
        "lastName": "fusaro",
    },
    "contact": {
        "email": "rfusaro12@gmail.com",
        "phone": "1345672389"
    },
    "role": "admin",
    "company": "hdaf6sdfsdf7sdf7sdfsdkj",
    "password": password,
    "userCode": "oistdgets",
    "slug": "dfsdf-sdfdsf-sdff",
    "passwordChange": "23/10/2023 12:50:23",
    "updateAt": "23/10/2023 12:50:23"
})

'''




'''
#*RESET
for collection in COLLECTIONS: 
    DB[collection].delete_many({})



#*CHECK PASSWORD
password0 = "password"
passw = DB[COLLECTIONS[7]].find_one({"userCode": "oistdgets"})


if bcrypt.checkpw(password0.encode('utf-8'), passw['password']):
    print("\nLa password è corretta!")
else:
    print("\nLa password non è corretta.")

#*SET PASSWORD
password = "password"
password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)
print(password)

DB = client[DATABASE[1]]

DB[COLLECTIONS[7]].delete_many({})

collection7 = DB[COLLECTIONS[7]]
collection7.insert_one({
    "photo": "photo.png",
    "businessRole": "ceo",
    "active": True,
    "validated": True,
    "createAt": "23/10/2023 12:50:23",
    "name": {
        "firstName": "riccardo",
        "lastName": "fusaro",
    },
    "contact": {
        "email": "rfusaro12@gmail.com",
        "phone": "1345672389"
    },
    "role": "admin",
    "company": "hdaf6sdfsdf7sdf7sdfsdkj",
    "password": password,
    "userCode": "oistdgets",
    "slug": "dfsdf-sdfdsf-sdff",
    "passwordChange": "23/10/2023 12:50:23",
    "updateAt": "23/10/2023 12:50:23"
})




#*ESEMPI DI QUERY
#SITO DOCS: https://pymongo.readthedocs.io/en/stable/

#Trova tutti i documenti in una collezione
    cursor = collection.find()

#Trova un documento specifico basato su un criterio
    filtro = {"campo": "valore"}
    cursor = collection.find(filtro)

#Seleziona solo alcuni campi dei documenti
    proiezione = {"campo1": 1, "campo2": 1, "_id": 0}
    cursor = collection.find(filtro, proiezione)

#Ordina i risultati in base a un campo specifico
    ordinamento = [("campo", pymongo.ASCENDING)]
    cursor = collection.find().sort(ordinamento)

#Limita il numero di documenti restituiti
    limite = 10
    cursor = collection.find().limit(limite)

#Esempi di operatori di confronto
    # Maggiore di
    filtro = {"campo": {"$gt": 5}}
    # In un intervallo
    filtro = {"campo": {"$gte": 5, "$lte": 10}}
    # Corrispondenza a un elenco di valori
    filtro = {"campo": {"$in": [valore1, valore2]}}

#Esegui una ricerca di testo completo
    filtro = {"$text": {"$search": "parola_chiave"}}
    cursor = collection.find(filtro, {"score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})])







'''

     