import spacy
from collections import Counter
import pandas as pd
from matplotlib import pyplot as plt

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 5000000

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Verarbeitung des Textes mit spaCy
docs = [nlp(text) for text in data['Text']]
years = data['Jahr']
parties = data['Partei']

# Identifizieren und Zählen von Superlativen pro Jahr und Partei
yearly_party_superlative_count = Counter()
for doc, year, party in zip(docs, years, parties):
    superlative_count = Counter()
    for token in doc:
        if token.pos_ == "ADJ" and "Sup" in token.morph.get("Degree", []):
            superlative_count[token.text] += 1
    yearly_party_superlative_count[(year, party)] += sum(superlative_count.values())

# Konvertieren der aggregierten Daten in einen DataFrame
yearly_party_superlative_df = pd.DataFrame(list(yearly_party_superlative_count.items()), columns=['Jahr_Partei', 'Häufigkeit_Superlative'])

# Aufteilen der kombinierten Spalte 'Jahr_Partei' in separate Spalten für Jahr und Partei
yearly_party_superlative_df[['Jahr', 'Partei']] = pd.DataFrame(yearly_party_superlative_df['Jahr_Partei'].tolist(), index=yearly_party_superlative_df.index)

# Tabelle anzeigen
print(yearly_party_superlative_df)

# Visualisierung der Anzahl der Imperativsätze pro Jahr und Partei in einem Lininendiagramm
#plt.figure(figsize=(10, 6))
#for party in yearly_party_superlative_df['Partei'].unique():
 #   party_data = yearly_party_superlative_df[yearly_party_superlative_df['Partei'] == party]
  #  plt.plot(party_data['Jahr'], party_data['Häufigkeit_Superlative'], label=party)
#plt.xlabel('Jahr')
#plt.ylabel('Anzahl der Superlative')
#plt.title('Anzahl der Superlative pro Jahr und Partei')
#plt.legend()
#plt.show()

# Daten für die Tabelle
table_data = yearly_party_superlative_df.pivot(index='Partei', columns='Jahr', values='Häufigkeit_Superlative')

# Erstellen der Tabelle
plt.figure(figsize=(10, 6))
plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center')

# Formatierung der Tabelle
plt.axis('off')
plt.title('Häufigkeit der Superlative pro Jahr und Partei')
plt.show()
