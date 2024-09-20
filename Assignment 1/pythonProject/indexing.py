#-------------------------------------------------------------------------
# AUTHOR: Jahin Mahbub
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 5180- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {?}

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {?}

#Identifying the index terms.
#--> add your Python code here
terms = []

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []

#Printing the document-term matrix.
#--> add your Python code here