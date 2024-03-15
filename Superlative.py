# Dieses Skript zählt die Superlative, die jährlich von CDU/CSU und Linken während der Reden gemacht wurden. Die Visualisierung wird über eine Tabelle gemacht. 

import spacy
from collections import Counter
import pandas as pd
from matplotlib import pyplot as plt

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 5000000

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Verarbeitung des Textes mit spaCy
docs = [nlp(text) for text in data['Text']]
jahre = data['Jahr']
parteien = data['Partei']

# Identifizieren und Zählen von Superlativen pro Jahr und Partei
zähler_superlative_jahr_partei = Counter()
for doc, year, party in zip(docs, jahre, parteien):
    zähler_superlative = Counter()
    for token in doc:
        if token.pos_ == "ADJ" and "Sup" in token.morph.get("Degree", []):
            zähler_superlative[token.text] += 1
    zähler_superlative_jahr_partei[(year, party)] += sum(zähler_superlative.values())

# Konvertieren der aggregierten Daten in einen DataFrame
superlative_jahr_partei_df = pd.DataFrame(list(zähler_superlative_jahr_partei.items()), columns=['Jahr_Partei', 'Häufigkeit_Superlative'])

# Aufteilen der kombinierten Spalte 'Jahr_Partei' in separate Spalten in Jahr und Partei
superlative_jahr_partei_df[['Jahr', 'Partei']] = pd.DataFrame(superlative_jahr_partei_df['Jahr_Partei'].tolist(), index=superlative_jahr_partei_df.index)

# Tabelle anzeigen
print(superlative_jahr_partei_df)

# Daten für die Tabelle
table_data = superlative_jahr_partei_df.pivot(index='Partei', columns='Jahr', values='Häufigkeit_Superlative')

# Erstellen der Tabelle
plt.figure(figsize=(10, 6))
plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center', bbox=[0.0,-1,1,1])

# Formatierung der Tabelle
plt.axis('off')
plt.title('Häufigkeit der Superlative pro Jahr und Partei')
plt.subplots_adjust(top=0.92) #Tabelle nach oben verschieben
plt.tight_layout() #Abstand der Tabelle und der Überschrift verringern
plt.show()
