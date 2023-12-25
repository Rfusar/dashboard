def Gestione(azione, DB, render_template, ID, session, l, usersL):
    def indirizzamento_utente():
        return {
            "Nmes" : l, 
            "N_amici": usersL -1, 
            "amici": session.get('users'), 
            "links": [], 
            "user": user,
            "azienda": azienda,
            "nome": session.get('utente')['utente']['identificazione']['nome'], 
            "check": session.get('demo'), 
            "ruolo": session.get("demo"), 
            "ragionesociale": session.get('utente')['azienda']['nome'],
            "tiks": tiks
        }
    def indirizzamento_azienda():
        return {
            "Nmes": l, 
            "N_amici": usersL -1,
            "check": session.get('demo'),
            "nome": session.get('utente')['utente']['identificazione']['nome'],
            "ragionesociale": session.get('utente')['azienda']['nome'],
            "azienda": azienda,
            "user": datiUser,
            "docs": docs,
            "ruolo": session.get("demo"),
            "tiks": tiks
        }


    #*-------------------------------------------------------------------------------------------------- UTENTE
    if azione[-1] == "e":
        datiUSER = DB['users'].find()
        for i in datiUSER:
            if str(i['_id']) == ID:  
                id = i['_id']
        user = DB['users'].find_one({'_id': id})
        azienda = DB['companies'].find_one({"_id": user['company']})
        tiks = [["sadas","blalbab","attivo","gigino","22/03/2023"],
            ["sadas","blalbab","non attivo","---","23/12/2023"],
            ["sadas","blalbab","attivo","gigino","22/03/2022"],
            ["sadas","blalbab","attivo","gigino","22/03/2022"],
                ["sadas","blalbab","non attivo","---","22/03/2022"]]
        
        if azione == "modificaUtente":
            return render_template("Admin/modifica_utente.html", **indirizzamento_utente())
            
        elif azione == "dettaglioUtente":
            return render_template("area_utente.html", **indirizzamento_utente())
    #*-------------------------------------------------------------------------------------------------- AZIENDA
    elif azione[-1] == "a":
        datiAzienda = DB['companies'].find()
        for i in datiAzienda:
            if str(i['_id']) == ID: 
                id = i['_id']
        azienda = DB['companies'].find_one({"_id":id})
        datiUser = DB['users'].find({'company': id}, {"password": 0})
        docs = [["sadas","titoli1","22/03/2022"], ["sadas","titoli1","22/03/2022"], ["sadas","titoli1","22/03/2022"]]
        tiks = [["sadas","attivo","22/03/2022"],["sadas","non attivo","22/03/2022"],["sadas","attivo","22/03/2022"]]
        
        if azione == "modificaAzienda":
            return render_template("Admin/modifica_azienda.html", **indirizzamento_azienda())

        elif azione == "dettaglioAzienda":
            return render_template("area_azienda.html", **indirizzamento_azienda())