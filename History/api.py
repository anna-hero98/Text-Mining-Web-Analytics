#dieses Modul macht Python fähig Internetadressen/requests rauszuschicken und zu empfangen
import requests
import spacy
import json
import jsonpath_ng as jp

#nlp = spacy.load("de_core_news_sm")

headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'
response = requests.get(url, headers=headers)

json_data = str(response.json())
#print(json_data)


json_object = json.dumps(json_data)
query1 = jp.parse("$.text")
result = query1.find(json_object)

print(result[0].value)

"""doc = nlp(json_data)

nomen = 0
for token in doc:
    #print(token.text, token.lemma_, token.pos_)
    if token.pos_ =="NOUN":
       nomen += 1
print("Nomen im Text: ", nomen)
print("Worte in Text: ", len(doc))




#apikey = "rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF"

#url =  'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.id=908&format=json&apikey=rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'
#data = requests.get(url).json()


# dieses Modul macht Python fähig requests an Endpunkte rauszuschicken und die Response zu empfangen
import requests
import json
import unicodedata
from spacy.lang.en.tokenizer_exceptions import string

idProtocol = 906
Dokumentennummer ='17/115'
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text/?f.dokumentnummer={Dokumentennummer}'
#url = f'https://search.dip.bundestag.de/api/v1/drucksache-text?f.dokumentnummer={Dokumentennummer}'
response = requests.get(url, headers=headers)

json_data =response.json()
if 'documents' in json_data:
    for document in json_data['documents']:
        text = document['text']
        if



obj = requests.get(url, headers=headers)
def extract_values(obj, key):
    #Pull all values of specified key from nested JSON.
    arr = []

    def extract(obj, arr, key):
        #Recursively search for values of key in JSON tree.
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

values = extract_values(json_object, 'title')
print(values)

response_data = json_object.json()
#print(response_data["id"])
#print(json_object.status_code)
#print(json_object.json())
#text = (response['text'])
#print(text)
#print(unicodedata.normalize('NFKC',str(response.json())))


#unicodedata.normalize

 """
