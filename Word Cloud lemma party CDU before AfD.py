import collections
import requests
import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib. pyplot as plt

nlp = spacy.load("de_core_news_sm")
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

import pandas as pd
import spacy
from collections import Counter

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 49027203

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")
vornamen = pd.read_csv("vornamen.csv")

# Extrahieren der Vornamen aus der CSV-Datei
vornamen_liste = vornamen["vorname"].tolist()

# Filtern auf die Partei
data_party_linke = data[(data['Partei'] == "CDU/CSU") & (data['Jahr'] < 2017)]

# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
text = " ".join(data_party_linke['Text'])

# spaCy-Verarbeitung
doc = nlp(text)

# Lemmatisierung und Frequenzzählung
lemmas = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and token.text.lower() not in ["beifall", "ausschuss", "drucksache"] and token.text.lower() not in vornamen_liste]
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

