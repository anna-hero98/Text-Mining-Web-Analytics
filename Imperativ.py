import requests
import spacy
from collections import Counter

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")

# Headers für die API-Anfrage
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

# Eingabe der Dokumentnummer
Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'
response = requests.get(url, headers=headers)

json_data = response.json()

if 'documents' in json_data:
    for document in json_data['documents']:
        text = document['text']

        # 1. Segmentierung des Textes in Sätze und Tokens
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]

        imperative_sentences = []

        # 2. Anwenden des POS-Taggers und Identifizieren von Imperativsätzen
        for sentence in sentences:
            sentence_doc = nlp(sentence)
            first_token_pos = sentence_doc[0].pos_
            last_token_text = sentence_doc[-1].text
            last_token_pos = sentence_doc[-1].pos_

            if (last_token_text.endswith('.') or last_token_text.endswith('!')) and first_token_pos == 'VERB':
                imperative_sentences.append(sentence)

        # 3. Ausgabe der identifizierten Imperativsätze
        if imperative_sentences:
            print("Identifizierte Imperativsätze:")
            for i, sentence in enumerate(imperative_sentences, 1):
                print(f"{i}. {sentence}")
        else:
            print("Keine Imperativsätze gefunden.")

else:
    print("Keine Dokumente gefunden.")