#dieses Modul macht Python fähig Internetadressen/requests rauszuschicken und zu empfangen
import requests
import spacy
import json
import jsonpath_ng as jp

nlp = spacy.load("de_core_news_sm")

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
#data = requests.get(url).json()"""
