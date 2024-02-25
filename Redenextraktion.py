import requests
import spacy

# Laden des SpaCy-Modells für die deutsche Sprache
nlp = spacy.load("de_core_news_sm")

# API-Anfrage
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
else:
    print("No documents found.")

# Analyse des Textes mit SpaCy
doc = nlp(text)

# Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
search_sentence = "Dritten Gesetzes zur Änderung des Aufstiegsfortbildungsförderungsgesetzes"
start = "Feist (CDU/CSU):"
parteien = ["(CDU/CSU):","(DIE LINKE):","(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"]

count_search_sentence = 0
count_partei = 0

# Finden der Startposition der gesuchten Wortreihenfolge
for sent in doc.sents:
    if search_sentence in sent.text:
        count_search_sentence += 1
        if count_search_sentence == 2:
            # Finden der Startposition der gesuchten Wortreihenfolge
            start_position = text.find(start)
            # -1 ist ein spezieller Wert für "nicht gefunden" oder "nicht vorhanden"
            if start_position != -1:
                # Wenn die gesuchte Wortreihenfolge gefunden wurde, dann Abgleich mit Parteien Liste
                for partei in parteien:
                    count_partei += 1
                    if count_partei == 2:
                        end_position = text.find(partei, start_position)
                        if end_position != -1:
                            # Wenn die nachfolgende Wortfolge gefunden wurde
                            desired_text = text[start_position:end_position]
                            print(desired_text)
                            break
                else:
                    # Wenn die nachfolgende Wortfolge nicht gefunden wurde
                    print("Die nachfolgende Wortfolge wurde nicht gefunden.")
            else:
                # Wenn die gesuchte Wortreihenfolge nicht gefunden wurde
                print("Die gesuchte Wortreihenfolge wurde nicht gefunden.")



"""
# Check if 'documents' key exists in json_data
if 'documents' in json_data:
    # Iterate over each document
    for document in json_data['documents']:
        # Access the 'text' field for each document
        text = document['text']
        print(text)
else:
    print("No documents found.")

doc = nlp(text)

Parteien = ["(CDU/CSU):","(DIE LINKE):","(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"]

# Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
search_sentence = "Dritten Gesetzes zur Änderung des Aufstiegsfortbildungsförderungsgesetzes"
Anfang = "Feist (CDU/CSU):"
following_sequence = "(DIE LINKE):"

count_search_sentence = 0

# Finden der Startposition der gesuchten Wortreihenfolge
for sent in doc.sents:
    if search_sentence in sent.text:
        count_search_sentence += 1
        if count_search_sentence == 2:
            # Finden der Startposition der gesuchten Wortreihenfolge
            start_position = text.find(Anfang)
            # -1 ist ein spezieller Wert für "nicht gefunden" oder "nicht vorhanden"
            if start_position != -1:
                # Wenn die gesuchte Wortreihenfolge gefunden wurde
                end_position = text.find(following_sequence, start_position)
                if end_position != -1:
                    # Wenn die nachfolgende Wortfolge gefunden wurde
                    desired_text = text[start_position:end_position]
                    print(desired_text)
                else:
                    # Wenn die nachfolgende Wortfolge nicht gefunden wurde
                    print("Die nachfolgende Wortfolge wurde nicht gefunden.")
            else:
                # Wenn die gesuchte Wortreihenfolge nicht gefunden wurde
                print("Die gesuchte Wortreihenfolge wurde nicht gefunden.")

"""