import tiktoken

USER_GPT ='''estrai le seguenti informazioni di questo testo.
tipo di contratto
istituto di credito mutuante
mutuatari/o
codice fiscale mutuatario
data erogazione
importo
durata
tasso fisso/variabile
importo iscrizione ipoteca volontaria
grado ipoteca
importo fideiussione
fideiussore/i
nr beni ipotecati
indirizzo beni ipotecati
categoria catastale
foglio
particella
mappale
il risultato lo trasformi in json trasformando il nome dei campi estratti in chiavi. indicati DOPO il carattere '=' come segue;
tipo di contratto=doctype
istituto di credito mutuante=creditinstitute
mutuatari/o=borrower
codice fiscale mutuatario=borrowerfiscalcode
data erogazione=emissiondate
importo=amount
durata=duration
tasso fisso/variabile=taxtype
importo iscrizione ipoteca volontaria=ipoteca
grado ipoteca=typeipoteca
importo fideiussione=fideiussione
fideiussore/i=fideiussore
nr beni ipotecati=numberbuilding
indirizzo beni ipotecati=addressbuilding
categoria catastale=category
foglio=paper
particella=particel
mappale=map'''

#*funzioni che servono --- QUALE SCEGLIERE?

def N_token_cl100k_base(a):
    enc = tiktoken.get_encoding("cl100k_base")
    token = len(enc.encode(a))

    return token

def N_token_p50k_base(a):
    enc = tiktoken.get_encoding("p50k_base")
    token = len(enc.encode(a))
    
    return token

def N_token_r50k_base(a):
    enc = tiktoken.get_encoding("r50k_base")
    token = len(enc.encode(a))

    return token


def N_token_p50k_edit(a):
    enc = tiktoken.get_encoding("p50k_edit")
    token = len(enc.encode(a))

    return token

