import pandas as pd
from collections import Counter
import spacy
import matplotlib.pyplot as plt


# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Filtern der Daten für Jahre kleiner als 2016
filtered_data = data[data['Jahr'] < 2017]

# Initialisierung der Zähler für Wortarten pro Partei
counter_per_party_word_type = {}

# Durchlaufen der gefilterten Daten
for text, party in zip(filtered_data['Text'], filtered_data['Partei']):
    # Initialisierung des Zählers für die aktuelle Partei
    if party not in counter_per_party_word_type:
        counter_per_party_word_type[party] = Counter()

    # spaCy-Verarbeitung
    doc = nlp(text)

    # Zählen der Wortarten im aktuellen Dokument
    word_types = ['NOUN', 'VERB', 'ADJ', 'ADV']
    for word_type in word_types:
        word_count = len([token.text for token in doc if token.pos_ == word_type])
        counter_per_party_word_type[party][word_type] += word_count

# Konvertieren der aggregierten Daten in einen DataFrame
party_word_type_df = pd.DataFrame(counter_per_party_word_type).T

# Tabelle anzeigen
print(party_word_type_df)

# Daten für die Tabelle
#table_data = party_word_type_df.pivot(index=['NOUN', 'VERB', 'ADJ', 'ADV'], columns='Partei', values='counter_per_party_word_type')

# Erstellen der Tabelle mit Matplotlib
plt.figure(figsize=(10, 6))
ax = plt.subplot(111)
ax.axis('off')  # Deaktivieren der Achsen
ax.table(cellText=party_word_type_df.values, rowLabels=party_word_type_df.index, colLabels=party_word_type_df.columns, loc='center')
plt.title('Häufigkeit der Wortarten pro Partei vor Eintritt der AfD ins Parlament')
plt.show()