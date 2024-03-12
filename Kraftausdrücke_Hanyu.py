import spacy
import nltk
import pandas as pd
import re
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 500000000000

# Laden der CSV-Datein
data = pd.read_csv("extracted_data_new_version.csv", sep=';')
kraftausdruecke_data = pd.read_csv("Kraftausdruecke.csv", sep=';')

# Für die Speicherung der Liste der Kraftausdrücke
kraftausdruecke_list = []

for row in kraftausdruecke_data['Kraftausdruecke']:
    kraftausdruecke_list.append(row)  # 1, da Anfang in Zeile 2 nach Überschrift
#print(kraftausdruecke_list)

anzahl_treffer = 0

for idx, (jahr, partei, thema, text) in enumerate(zip(data['Jahr'], data['Partei'], data['Thema'], data['Text'])):
    # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
    for kraftausdruck in kraftausdruecke_list:
        if kraftausdruck in text:
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z]+\. )', text)
            print(f"{kraftausdruck} gefunden in Zeile: {idx}\n Jahr: {jahr} Partei: {partei}  Thema: {thema}\n")
            anzahl_treffer += 1
            text =

print(anzahl_treffer)