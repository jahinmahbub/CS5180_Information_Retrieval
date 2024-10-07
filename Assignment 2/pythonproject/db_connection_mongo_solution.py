from pymongo import MongoClient
import datetime
from collections import defaultdict

def connectDataBase():
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    document = {
        "_id": int(docId),
        "text": docText,
        "title": docTitle,
        "date": datetime.datetime.strptime(docDate, "%Y-%m-%d"),
        "category": docCat
    }
    col.insert_one(document)

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    updated_data = {
        "$set": {
            "text": docText,
            "title": docTitle,
            "date": datetime.datetime.strptime(docDate, "%Y-%m-%d"),
            "category": docCat
        }
    }
    col.update_one({"_id": int(docId)}, updated_data)

def deleteDocument(col, docId):
    col.delete_one({"_id": int(docId)})

def getIndex(col):
    index = defaultdict(list)
    documents = col.find()

    for doc in documents:
        terms = doc['text'].lower().split()  # Split text into terms
        for term in set(terms):  # Unique terms for each document
            index[term].append(f"{doc['title']}:{doc['_id']}")

    # Format index: {term: 'title:ID, ...'}
    formatted_index = {term: ', '.join(value) for term, value in index.items()}
    return formatted_index