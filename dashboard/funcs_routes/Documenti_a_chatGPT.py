#*LAVORAZIONE
def lavorazione_foglio(re, testo, N_token_cl100k_base):
    pattern= r"[a-zA-Z0-9\" \".,;:_\n-<>]"
    p = re.findall(pattern, testo)

    testo_formattato = "".join(p)
    system_gpt = testo_formattato.replace("\n", "")

    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\SYSTEM.txt", "w", encoding="utf-8") as f: f.write(system_gpt)
    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\SYSTEM.txt", encoding="utf-8") as f: SYSTEM_GPT = f.read()

    a = N_token_cl100k_base(SYSTEM_GPT)
    ogg={
        "SYSTEM" : {
            "scritto su file":{
                "cl100k_base": a,
                "lunghezza": len(SYSTEM_GPT)
            }
        }
    }
    mess = {
        "testo": SYSTEM_GPT, 
        "token":ogg,            
    }
        
    return mess

def lavorazione_folder(request, re, N_token_cl100k_base, jsonify):
    uploaded_files = request.files.getlist('file')
        
    file_contents = []
    #lettura
    for file in uploaded_files:
        pattern= r"[a-zA-Z0-9\" \".,;:_\n-<>]"
        p = re.findall(pattern, file.read().decode('utf-8'))

        testo_formattato = "".join(p)
        SYSTEM_GPT = testo_formattato.replace("\n", "")

        o = file.filename.find('/')

        file_contents.append({
            'filename': file.filename[o+1:-4],
            'content': SYSTEM_GPT
        })
    #lavorazione
    dati_file = []
    n = 0
    for file in file_contents:
        token = N_token_cl100k_base(file['content'])
        n+=1
        dati_file.append({
            "documento": {
                "token": token,
                "contenuto": file['content'],
                "nome": file['filename'],
                "n_char": len(file['content'])
            },
            "folder": f"{n}/{len(file_contents)}"
        })
    return jsonify(dati_file)
    


#*DARE A chatGPT
def dare_foglio(system_gpt, user_gpt, TITOLO):
    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\SYSTEM.txt", "w", encoding="utf-8") as f: f.write(system_gpt)
    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\SYSTEM.txt", encoding="utf-8") as f: SYSTEM_GPT = f.read()
    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\USER.txt", "w", encoding="utf-8") as f: f.write(user_gpt)
    with open("C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\USER.txt", encoding="utf-8") as f: USER_GPT = f.read()
    '''
    try: 
        risposta = interact_with_chatgpt_prova(USER_GPT, SYSTEM_GPT, api_key, maxContent, creativita)
        cur = connPOSTGRES.cursor()
        cur.execute('INSERT INTO documenti (documento, token, nome_file) VALUES (%s,%s, %s)',(risposta[0],risposta[1], TITOLO))
        connPOSTGRES.commit()
        cur.close()

        return {"status": f"{TITOLO}, eseguito"}
        
    except Exception as e:
        return {"status":f"{e}"}
    '''
    return {"status": f"{TITOLO}, eseguito"}

def dare_folder(dati):
    secondiTOT = 25 * len(dati.get('documenti'))
    secondi = secondiTOT % 60
    minuti = secondiTOT / 60
    USER_GPT = dati.get("comando")

    for i in dati.get('documenti'):
        TITOLO = i['titolo']
        SYSTEM_GPT = i['contenuto']
        #PROVA
        with open(f"C:\\Users\\Utente\\Desktop\\presenze_lavoro\\esercizi\\progettoAndrea2\\prova_lettura_cartella\\{TITOLO}.txt", "w") as f:
            f.write(f"{USER_GPT}\n\n")
            f.write(SYSTEM_GPT)

        '''
        try: 
            risposta = interact_with_chatgpt_prova(USER_GPT, SYSTEM_GPT, api_key, maxContent, creativita)
            cur = connPOSTGRES.cursor()
            cur.execute('INSERT INTO documenti (documento, token, nome_file) VALUES (%s,%s,%s)',(risposta[0], risposta[1], TITOLO))
            connPOSTGRES.commit()
            cur.close()

        except Exception as e:
            return {"err": f"{e}"}
        '''
                 
    return {"status": f"aspetta circa 20/25sec per documento, cioè {int(minuti)}m {secondi}sec circa"}