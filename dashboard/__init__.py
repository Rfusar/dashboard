from flask import Flask
import py7zr
from getpass import getpass



def estrai_file_7zip(file_archivio, password):
    try:
        with py7zr.SevenZipFile(file_archivio, mode='r', password=password) as z:
            z.extractall(path="C:\\Users\\Utente\\Desktop\\info\\variabili")
            print("Contenuto estratto con successo.")
            return True
    except py7zr.Bad7zFile:
        print("Errore: File 7z danneggiato o password errata.")
        return False

count = ""
path = "C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettiAndrea\\Repository_GDPR"
with open(path+"\\check.txt", "r") as f: count = f.read()


#*INIZIO
with open("C:\\Users\\Utente\\Desktop\\info\\variabili\\prova.txt") as f: PASSWORD = f.read()
VALORE = None
if count == "True":
    print("stai sviluppando oppure deve lavorare??")
    risposta = input(": ")
    if risposta == "sto sviluppando": VALORE = False
    elif risposta == "deve lavorare": VALORE = True

elif count == "False": VALORE = False


with open(path+"\\check.txt", "w") as f: count = f.write("False")
file_archivio = "C:\\Users\\Utente\\Desktop\\info\\variabili\\.env.7z" 

password = getpass("Inserisci la password dell'archivio 7z: ") if VALORE else PASSWORD

if estrai_file_7zip(file_archivio, password):
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    from dashboard import routes
