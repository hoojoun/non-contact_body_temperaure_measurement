import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Certificate and initialize firebase DB
cred = credentials.Certificate("ondocha-2ce69-firebase-adminsdk-quvpb-4aa50f6762.json")
firebase_admin.initialize_app(cred,{'projectID':'ondocha-2ce69',})

#Save Data
db=firestore.client()
doc_ref=db.collection(u'Root').document(u'Visitor_Info').collection(u'20201010').document(u'1111')
doc_ref.set({
    u'Code':"3",    
    u'Ftem':37.8,
    u'Wtem':38.0,
    u'date':"20211010",
    u'time':"1413"
})
