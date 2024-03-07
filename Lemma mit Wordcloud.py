import collections

import requests
import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib. pyplot as plt

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

        # Lemmatisierung und Frequenzzählung
        lemmas = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
        lemma = collections.Counter(lemmas)
        lemma_freq = Counter(lemmas)

        wc = WordCloud().generate_from_frequencies(lemma_freq)
        plt.imshow(wc)
        plt.show()

        # Sortieren der Frequenzen in absteigender Reihenfolge
        for lemma, freq in lemma_freq.most_common():
            print(f"{lemma}: {freq}")
else:
    print("Keine Dokumente gefunden.")
