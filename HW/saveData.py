import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def saveFireBase1(code,name,atem,ftem="null"):
    #save Date
    import time
    now=time.localtime()
    date=str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)
    time=str(now.tm_hour)+str(now.tm_min)
    
    #Certificate and initialize firebase DB
    cred = credentials.Certificate("ondocha-2ce69-firebase-adminsdk-quvpb-4aa50f6762.json")
    firebase_admin.initialize_app(cred,{'projectID':'ondocha-2ce69',})

    #Save Data1
    docuCode=code+"_"+date+"_"+time
    db=firestore.client()
    doc_ref=db.collection(u'Root').document(u'Visitor_Info').collection(date).document(docuCode)# test code
    doc_ref.set({
        u'Code':code,    
        u'Ftem':ftem,
        u'Atem':atem,
        u'date':date,
        u'time':time,
    })

def saveFireBase2(code,name,atem,ftem="null"):
    #save Date
    import time
    now=time.localtime()
    date=str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)
    time=str(now.tm_hour)+str(now.tm_min)
    
    
    #Certificate and initialize firebase DB
    cred = credentials.Certificate("ondocha-2ce69-firebase-adminsdk-quvpb-4aa50f6762.json")
    firebase_admin.initialize_app(cred,{'projectID':'ondocha-2ce69',})
    #Save Data1
    docuCode=code+"_"+date+"_"+time
    db=firestore.client()
    doc_ref=db.collection(u'Root').document(u'Visitor_Info').collection(date).document(docuCode)# test code
    doc_ref.set({
        u'Code':code,    
        u'Ftem':ftem,
        u'Atem':atem,
        u'date':date,
        u'time':time,
    })
    #Save Data2
    db=firestore.client()
    doc_ref=db.collection(u'Root').document(u'Suspected').collection(u'Info').document(docuCode)
    doc_ref.set({
        u'Code':code,
        u'Name':name,
        u'Ftem':ftem,
        u'Atem':atem,
        u'date':date,
        u'time':time,
        u'Confirmed':bool(0),
        u'Disinfection':bool(0),
        u'Memo':"",
    })
