import requests
import spacy
import pandas as pd

#nlp = spacy.load("de_core_news_sm")
file_path_speeches = 'Erster_Teil_Reden.csv'
df = pd.read_csv(file_path_speeches, sep=',')
print(df.head())
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'
response = requests.get(url, headers=headers)

json_data = response.json()

# Check if 'documents' key exists in json_data
if 'documents' in json_data:
    # Iterate over each document
    for document in json_data['documents']:
        # Access the 'text' field for each document
        text = document['text']
        #for line in text:
            #if "" in line:

        # Now you can use the 'text' variable for further processing
        print(text)
else:


    print("No documents found.")