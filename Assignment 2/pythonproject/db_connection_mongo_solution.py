from pymongo import MongoClient
import datetime
from collections import defaultdict

client = None  # Define a global client variable

def connectDataBase():
    global client
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

def closeConnection():
    if client:
        client.close()  # Explicitly close the connection
        print("MongoDB connection closed successfully.")

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
    # Perform an update by directly overwriting fields with $set
    col.update_one(
        {"_id": int(docId)},
        {
            "$set": {
                "text": docText,  # Set the new text as a string
                "title": docTitle,  # Set the new title as a string
                "category": docCat,  # Set the new category as a string
                "date": datetime.datetime.strptime(docDate, "%Y-%m-%d")  # Set the new date
            }
        }
    )

def deleteDocument(col, docId):
    col.delete_one({"_id": int(docId)})

def getIndex(col):
    index = defaultdict(list)
    documents = col.find()

    for doc in documents:
        terms = doc['text'].lower().split()
        for term in terms:
            index[term].append(f"{doc['title']}:{doc['_id']}")

    formatted_index = {term: ', '.join(value) for term, value in index.items()}
    return formatted_index