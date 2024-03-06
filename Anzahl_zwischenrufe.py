import requests
import spacy
from collections import Counter

# Laden des deutschen Sprachmodells
nlp = spacy.load("de_core_news_sm")
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'
response = requests.get(url, headers=headers)

json_data = response.json()

if 'documents' in json_data:
    for document in json_data['documents']:
        text = document['text']

        # spaCy-Verarbeitung
        doc = nlp(text)

        # Separates Zählen für jede Wortart
        nouns = Counter([token.text for token in doc if token.pos_ == "NOUN"])
        verbs = Counter([token.text for token in doc if token.pos_ == "VERB"])
        adjectives = Counter([token.text for token in doc if token.pos_ == "ADJ"])
        adverbs = Counter([token.text for token in doc if token.pos_ == "ADV"])

        # Ausgabe nach Wortart sortiert
        print("Substantive:")
        for word, freq in nouns.most_common():
            print(f"{word}: {freq}")

        print("\nVerben:")
        for word, freq in verbs.most_common():
            print(f"{word}: {freq}")

        print("\nAdjektive:")
        for word, freq in adjectives.most_common():
            print(f"{word}: {freq}")

        print("\nAdverbien:")
        for word, freq in adverbs.most_common():
            print(f"{word}: {freq}")

        print(f"Anzahl der Substantive: {sum(nouns.values())}")
        print(f"Anzahl der Verben: {sum(verbs.values())}")
        print(f"Anzahl der Adjektive: {sum(adjectives.values())}")
        print(f"Anzahl der Adverbien: {sum(adverbs.values())}")

    else:
        print("Keine Dokumente gefunden.")