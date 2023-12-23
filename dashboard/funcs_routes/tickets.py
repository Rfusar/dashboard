def gestione_Tickets___admin(DB, tiks):
    user = DB['users'].find({}, {'_id': 1, "name.firstName": 1, "name.lastName": 1})
    company = DB['companies'].find({}, {'_id': 1, "name": 1})
    tik = DB['tickets'].find()
    for i in tik:
        OGG={}
        OGG['title'] = i['title']
        OGG['status'] = i['status']
        OGG['ticketCode'] = i['ticketCode']
        OGG['createAt'] = i['createAt']
        for c in company:
            if i['company'] == c['_id']:
                OGG['company'] = c['name']

        for U in user:
            if i['assignedTO'] == U['_id']:
                OGG['person'] = f"{U['name']['firstName']} {U['name']['lastName']}"
        tiks.append(OGG)

def gestione_Ticktes___user(DB, tiks, email):
    user = DB['users'].find_one({{"contact.email": email}}, {'_id': 1, "name.firstName": 1, "name.lastName": 1, "company": 1})
    company = DB['companies'].find_one({"_id": user['company']}, {'_id': 1, "name": 1})
    tik = DB['tickets'].find()

    for i in tik:
        OGG={}
        OGG['title'] = i['title']
        OGG['status'] = i['status']
        OGG['ticketCode'] = i['ticketCode']
        OGG['createAt'] = i['createAt']
        OGG['company'] = company['name']
        if i['assignedTO'] == user['_id']:
                OGG['person'] = f"{user['name']['firstName']} {user['name']['lastName']}"
        tiks.append(OGG)