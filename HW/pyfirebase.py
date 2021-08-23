#-*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("testfb-455d9-firebase-adminsdk-4v8es-e0347f0252.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'testfb-455d9',
})

db = firestore.client()

doc_ref = db.collection(u'20210823').document(u'2017E')
doc_ref.set({
    u'Code': "2017E",
    u'Ftem': 36.5,
    u'Wtem': "null",
    u'name': "서호준",
    u'time': "1513"
})