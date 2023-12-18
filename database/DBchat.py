import glob
import sqlite3
from .DB import connPOSTGRES




def chat(utente1, utente2, mes1, mes2, data):
    cartella = '.chat'
    files = glob.glob(cartella + '/*.db')

    nomedb = f'.chat\\{utente1 + utente2}.db'
    dbnome = f'.chat\\{utente2 + utente1}.db'


    #AUTOMESSAGGIO
    if nomedb == dbnome:

        if nomedb in files:
            conn = sqlite3.connect(nomedb)

            cur = conn.cursor()
            cur.execute(f'INSERT INTO chat VALUES (?,?)', (mes1, data))
            conn.commit()
            cur.close()

        else:
            conn = sqlite3.connect(nomedb)
            cur = conn.cursor()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS chat(
                    {utente1} VARCHAR(255),
                    dataMes DATE NOT NULL
                ) 
            ''')
            conn.commit()

            cur.execute(f'INSERT INTO chat VALUES (?,?)', (mes1, data))
            conn.commit()
            cur.close()
        

    else:
        if nomedb in files or dbnome in files:
            # Il database esiste già, quindi connetti e inserisci i valori
            if nomedb in files:
                conn = sqlite3.connect(nomedb)

                cur = conn.cursor()
                cur.execute(f'INSERT INTO chat VALUES (?,?,?)', (mes1, mes2, data))
                conn.commit()
                cur.close()
            else:
                conn = sqlite3.connect(dbnome)

                cur = conn.cursor()
                cur.execute(f'INSERT INTO chat VALUES (?,?,?)', (mes2, mes1, data))
                conn.commit()
                cur.close()


        else:
            # Il database non esiste, quindi crea un nuovo database e una nuova tabella
            conn = sqlite3.connect(nomedb)
            cur = conn.cursor()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS chat(
                    {utente1} VARCHAR(255),
                    {utente2} VARCHAR(255),
                    dataMes DATE NOT NULL
                ) 
            ''')
            conn.commit()

            cur.execute(f'INSERT INTO chat VALUES (?,?,?)', (mes1, mes2, data))
            conn.commit()
            cur.close()
        






    
def readChat(utente1, utente2):

    class Mess():
        def __init__(self, io, tu):
            self.io = io
            self.tu = tu

        def invia(self):
            mess_dict = {
                f'{utente1}': self.io,
                f'{utente2}': self.tu
            }
            return mess_dict


    cartella = '.chat'
    files = glob.glob(cartella + '/*.db')

    nomedb = f'.chat\\{utente1 + utente2}.db'
    dbnome = f'.chat\\{utente2 + utente1}.db'

    n = []

    # CHECK
    if nomedb in files or dbnome in files:
        if nomedb in files:
            conn = sqlite3.connect(nomedb)

            cur = conn.cursor()
            cur.execute(f'SELECT {utente1}, {utente2} FROM chat')
            a = cur.fetchall()
            for i in a:
                b = Mess(i[0], i[1])
                n.append(b.invia())

            cur.close()
            return n 
        
        else:
            conn = sqlite3.connect(dbnome)

            cur = conn.cursor()
            cur.execute(f'SELECT {utente2}, {utente1} FROM chat')
            a = cur.fetchall()
            for i in a:
                b = Mess(i[1], i[0])
                n.append(b.invia())
            
            cur.close()
            return n 

    else:
        pass
















def notifica(utente1, mes1 ,data, attributo, RG):
    cartella = '.notifiche'
    files = glob.glob(cartella+'/*.db')

    nomedb = f'.notifiche\\{utente1}_{RG}.db'
   
    if nomedb in files:
        conn = sqlite3.connect(nomedb)

        cur = conn.cursor()
        cur.execute(f'INSERT INTO notifica VALUES (?,?,?,?)', (mes1, data, attributo,RG))
        conn.commit()
        cur.close()
        

    else:
        # Il database non esiste, quindi crea un nuovo database e una nuova tabella
        conn = sqlite3.connect(nomedb)
        cur = conn.cursor()
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS notifica(
                {utente1} VARCHAR(255),
                dataMes DATE NOT NULL,
                attributo INT,
                ragionesociale VARCHAR(100) 
            ) 
        ''')
        conn.commit()

        cur.execute(f'INSERT INTO notifica VALUES (?,?,?,?)', (mes1, data, attributo,RG))
        conn.commit()
        cur.close()
    


def readNotifica(utente1, RG):

    class Mess():
        def __init__(self, NOTIFICA, attributo, data,RG):
            self.NOTIFICA = NOTIFICA
            self.attributo = attributo
            self.data = data
            self.RG = RG
            


        def invia(self):
            mess_dict = {
                f'{utente1}': self.NOTIFICA,
                'attributo': self.attributo,
                'data' : self.data,
                'ragionesociale' : self.RG
     
            }
            return mess_dict


    cartella = '.notifiche'
    files = glob.glob(cartella + '/*.db')

    nomedb = f'.notifiche\\{utente1}_{RG}.db'
    

    n = []

    # CHECK
    if nomedb in files:
        conn = sqlite3.connect(nomedb)

        cur = conn.cursor()
        cur.execute(f'SELECT {utente1}, attributo, dataMes, ragionesociale FROM notifica')
        a = cur.fetchall()
        for i in a:
            b = Mess(i[0], i[1], i[2], i[3])
            n.append(b.invia())

        cur.close()
        return n  

    else:
        pass


def allNotifica(RG):

    n = []

    class Mess():
        def __init__(self, NOTIFICA, attributo, data,RG):
            self.NOTIFICA = NOTIFICA
            self.attributo = attributo
            self.data = data,
            self.RG = RG
            


        def invia(self):
            mess_dict = {
                'notifica': self.NOTIFICA,
                'attributo': self.attributo,
                'data' : self.data,
                'ragionesociale' : self.RG
                
     
            }
            return mess_dict
    
    curUNO = connPOSTGRES.cursor()
    curUNO.execute('SELECT nome FROM utenti WHERE ragionesociale = %s',(RG,))
    u = curUNO.fetchall()
    uL = len(u)
    curUNO.close()

    count = 0

    while count < uL:
        
        #SI POTREBBE FARE PER CARTELLE: files = cartella = f'.notifiche\\{RG}/*.db'
        cartella = '.notifiche'
        files = glob.glob(cartella + '/*.db')

        nomedb = f'.notifiche\\{u[count][0]}_{RG}.db'

        # CHECK
        if nomedb in files:
            conn = sqlite3.connect(nomedb)

            cur = conn.cursor()
            cur.execute(f'SELECT {u[count][0]}, attributo, dataMes, ragionesociale FROM notifica')
            a = cur.fetchall()
            for i in a:
                b = Mess(i[0], i[1], i[2], i[3])
                n.append(b.invia())

            cur.close()
                
        else:
            pass

        count += 1


    return n

