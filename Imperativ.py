
import pandas as pd
import spacy
import matplotlib.pyplot as plt
from zipfile import ZipFile

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Fehlende Werte entfernen und daraufhin Index zurücksetzen
data = data.dropna().reset_index(drop=True)

# Auf die Spalten "Text" und "Jahr" zugreifen
text_column = data['Text']
year_column = data['Jahr']

# Liste für die Anzahl der Imperativsätze für jedes Jahr
zähler_imperativ_jahr = {}

# Iteration über jeden Text und das entsprechende Jahr
for text, year in zip(text_column, year_column):
    # 1. Text in Sätze und Tokens segmentieren
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    imperativ = []

    # 2. Anwenden des POS-Taggers und Identifizieren von Imperativsätzen
    for sentence in sentences:
        sentence_doc = nlp(sentence)
        first_token_pos = sentence_doc[0].pos_
        last_token_text = sentence_doc[-1].text
        last_token_pos = sentence_doc[-1].pos_

        if (last_token_text.endswith('.') or last_token_text.endswith('!')) and first_token_pos == 'VERB':
            imperativ.append(sentence)

    # Anzahl der identifizierten Imperativsätze speichern
    zähler_imperativ = len(imperativ)

    # Aggregieren der Anzahl der Imperativsätze pro Jahr
    if year in zähler_imperativ_jahr:
        zähler_imperativ_jahr[year] += zähler_imperativ
    else:
        zähler_imperativ_jahr[year] = zähler_imperativ

# Konvertieren der aggregierten Daten in einen DataFrame für Visualisierung
imperativ_df = pd.DataFrame(list(zähler_imperativ_jahr.items()), columns=['Jahr', 'Anzahl_Imperativsätze'])

# Tabelle anzeigen
print(zähler_imperativ_jahr)

# Visualisierung der Anzahl der Imperativsätze pro Jahr
plt.bar(imperativ_df['Jahr'], imperativ_df['Anzahl_Imperativsätze'])
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Imperativsätze')
plt.title('Anzahl der Imperativsätze pro Jahr')
plt.show()

