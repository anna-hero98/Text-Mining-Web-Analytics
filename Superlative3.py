import requests
import spacy
from collections import Counter

# Laden des deutschen Sprachmodells
nlp = spacy.load("de_core_news_sm")

# Setzen der Header für die API-Anfrage
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

# Eingabe der Dokumentnummer
Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'

# Anfrage an die API
response = requests.get(url, headers=headers)
json_data = response.json()

if 'documents' in json_data:
    for document in json_data['documents']:
        text = document['text']

        # Verarbeitung des Textes mit spaCy
        doc = nlp(text)

    # Identifizieren und Zählen von Superlativen
    superlative_count = Counter()
    for token in doc: #geht jedes Token in dem durch eine NLP-Bibliothek vorverarbeiteten Dokument doc durch (Basis/Idee VL Slides)
        if token.tag_ == "ADJA" and token.morph.get("Degree") == ["Sup"]:
        #Überprüfung, ob das aktuelle Token ein adj. Superlativ ist.
        #1. wird geprüft, ob der POS-Tag (Part-of-Speech Tag) des Tokens ADJA (ein Adjektiv )ist
        #2. wird überprüft, ob das morphologische Merkmal Degree des Tokens den Wert Sup hat
        # --> Bedeutet, dass das Adjektiv in der Superlativform vorliegt.
            superlative_count[token.text] += 1

    # Ausgabe der Superlative und ihrer Häufigkeiten, absteigend sortiert
    print("Superlativ - Häufigkeit")
    for superlativ, haeufigkeit in superlative_count.most_common():
        print(f"{superlativ} - {haeufigkeit}")


## Visualiseurng der Ergebnisse --> Tabelle mit Anzahl. Zeitangabe (1x Tabelle: Vor AFD Eintritt)
## (1x Tabelle: Nach AFD Eintritt), mit Zeile pro Jahr + Häufigste Superlative auflisten



