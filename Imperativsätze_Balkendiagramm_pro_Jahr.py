import pandas as pd
import spacy
import matplotlib.pyplot as plt
from zipfile import ZipFile

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Benutzerdefinierte Behandlung fehlerhafter Zeilen
data = data.dropna().reset_index(drop=True)

# Auf die Spalten "Text" und "Jahr" zugreifen
text_column = data['Text']
year_column = data['Jahr']


# Neue Liste zur Speicherung der Anzahl der Imperativsätze für jedes Jahr
yearly_imperative_counts = {}

# Iteration über jeden Text und das entsprechende Jahr
for text, year in zip(text_column, year_column):
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

    # Anzahl der identifizierten Imperativsätze speichern
    imperative_count = len(imperative_sentences)

    # Aggregieren der Anzahl der Imperativsätze pro Jahr
    if year in yearly_imperative_counts:
        yearly_imperative_counts[year] += imperative_count
    else:
        yearly_imperative_counts[year] = imperative_count

# Konvertieren der aggregierten Daten in einen DataFrame
yearly_imperative_df = pd.DataFrame(list(yearly_imperative_counts.items()), columns=['Jahr', 'Anzahl_Imperativsätze'])

# Tabelle anzeigen
print(yearly_imperative_df)

# Visualisierung der Anzahl der Imperativsätze pro Jahr
plt.bar(yearly_imperative_df['Jahr'], yearly_imperative_df['Anzahl_Imperativsätze'])
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Imperativsätze')
plt.title('Anzahl der Imperativsätze pro Jahr')
plt.show()
