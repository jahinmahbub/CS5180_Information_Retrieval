#-------------------------------------------------------------------------
# AUTHOR: Jahin Mahbub
# FILENAME: Indexing2.py
# SPECIFICATION: Compute tf-idf
# FOR: CS 5180- Assignment #1
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

# Importing some Python libraries
import csv
import math

documents = []

# Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0])

# Conducting stopword removal for pronouns/conjunctions.
stopWords = {"i", "she", "he", "they", "and", "her", "their"}

# Conducting stemming. Hint: use a dictionary to map word variations to their stem.
stemming = {
    "cats": "cat",
    "loves": "love",
    "dogs": "dog"
}

# Helper function to preprocess the text (stopword removal + stemming)
def preprocess(doc):
    words = doc.lower().split()
    result = []
    for word in words:
        if word not in stopWords:  # Stopword removal
            stemmed_word = stemming.get(word, word)  # Apply stemming if applicable
            result.append(stemmed_word)
    return result

# Preprocess all documents
processed_docs = [preprocess(doc) for doc in documents]

# Identifying the index terms.
terms = sorted(set(word for doc in processed_docs for word in doc))

# Function to compute term frequency (TF), normalized by document length
def compute_tf(doc, term):
    term_count = doc.count(term)
    return term_count / len(doc)  # Normalizing by document length

# Function to compute inverse document frequency (IDF) with log base 10
def compute_idf(term, docs):
    doc_count = sum(1 for doc in docs if term in doc)
    return math.log10(len(docs) / doc_count) if doc_count > 0 else 0

# Building the document-term matrix by using the tf-idf weights.
docTermMatrix = []
idf_values = {term: compute_idf(term, processed_docs) for term in terms}

# Calculate the TF-IDF values for each document
for doc in processed_docs:
    tfidf_values = []
    for term in terms:
        tf = compute_tf(doc, term)
        tfidf = tf * idf_values[term]
        tfidf_values.append(tfidf)
    docTermMatrix.append(tfidf_values)

# Printing the document-term matrix.
print("Document-Term Matrix (TF-IDF):")
print(f"{'Terms':<10} {'d1':<10} {'d2':<10} {'d3':<10}")

for i, term in enumerate(terms):
    row = [f"{docTermMatrix[doc_idx][i]:<10.3f}" for doc_idx in range(len(docTermMatrix))]
    print(f"{term:<10} {' '.join(row)}")