import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

HOST = os.getenv('host')
USER = os.getenv('user')
PW = os.getenv('password')
DB = os.getenv('database')



connPOSTGRES = psycopg2.connect(

host = HOST,
user = USER,
password = PW,
database = DB
)



def copy_file(source_path, destination_path):
    try:
        with open(source_path, 'r') as source_file:
            content = source_file.read()

        
        with open(destination_path, 'w') as destination_file:
            destination_file.write(content)
        
        print("File copied successfully!")
    except Exception as e:
        print("An error occurred while copying the file:", str(e))

def checkToken(dati, MESI):
    dataset__dal_DB = []
    for i in dati:
        dati = {}
        dati['token'] = i[0]
        dati['quando'] = i[1]
        dataset__dal_DB.append(dati)

    anno_attuale = dt.now().year
    mese_attuale = dt.now().month
    giorno_attuale = dt.now().day

    dataset = {}
    Anno = []
    Mese = {}
    for n in range(0,12): Mese[MESI[n]] = []

    for i in dataset__dal_DB:
        anno = dt.strptime(str(i['quando']), '%Y-%m-%d').year
        mese = dt.strptime(str(i['quando']), '%Y-%m-%d').month
        giorno = dt.strptime(str(i['quando']), '%Y-%m-%d').day
        #se è di quest'anno
        if anno == anno_attuale:
            for n in range(1,13):
                if n == mese:
                    Mese[MESI[n-1]].append(i['token']) 
    Anno.append(Mese)

    for i in range(0,12):
        if Mese[MESI[i]]:
            som = 0
            for token in Mese[MESI[i]]:
                som += token
            Mese[MESI[i]] = som


    ultimo_check = []
    for i in Anno:
        for n in range(0,12):
            if i[MESI[n]] == []:
                ultimo_check.append(0)
            else:
                ultimo_check.append(i[MESI[n]])

    return ultimo_check