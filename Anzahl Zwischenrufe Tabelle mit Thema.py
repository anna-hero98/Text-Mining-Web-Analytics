#Dieses Skript zählt die Zwischenrufe, die von der CDU/CSU und den Linken für bestimmte Themen gemacht wurden. 
#Die Zwischenrufe werden dabei jeweils für den Zeitraum vor und nach 2017 betrachtet. Weiterhin werden die Ergebnisse in einer Tabelle visualisiert.
import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Initialisierung der Zähler pro Jahr und Thema für CDU/CSU und Die Linken
cdu_counts_per_year = {}
die_linke_counts_per_year = {}

# For Schleife über die CSV Daten mit dem Zähler der Zwischenrufe
for text, year, themes in zip(data['Text'], data['Jahr'], data['Thema']):
    # Initialisierung der Zähler für das aktuelle Jahr
    if year not in cdu_counts_per_year:
        cdu_counts_per_year[year] = {}
    if year not in die_linke_counts_per_year:
        die_linke_counts_per_year[year] = {}

    # Initialisierung der Themenzähler für das jeweilige Jahr
    for theme in themes.split(','):
        theme = theme.strip()  # Leerzeichen entfernen
        if theme not in cdu_counts_per_year[year]:
            cdu_counts_per_year[year][theme] = 0
        if theme not in die_linke_counts_per_year[year]:
            die_linke_counts_per_year[year][theme] = 0

        # Zählen der Zwischenrufe für CDU/CSU und Die Linke pro Thema
        cdu_counts_per_year[year][theme] += text.count("[CDU/CSU]:")
        die_linke_counts_per_year[year][theme] += text.count("[DIE LINKE]:")

# Erstellen einer DataFrame für die Anzeige der Ergebnisse in einer Tabelle
table_data_cdu = pd.DataFrame(cdu_counts_per_year).fillna(0).astype(int)
table_data_linke = pd.DataFrame(die_linke_counts_per_year).fillna(0).astype(int)

# Sortieren der Spalten (Jahre) in aufsteigender Reihenfolge
table_data_cdu_sorted = table_data_cdu.sort_index(axis=1)
table_data_linke_sorted = table_data_linke.sort_index(axis=1)

# Transponieren der DataFrames
table_data_cdu_transposed = table_data_cdu_sorted.T
table_data_linke_transposed = table_data_linke_sorted.T

# Umwandeln der Jahre in Zeichenfolgen
table_data_cdu_transposed.columns = table_data_cdu_transposed.columns.astype(str)
table_data_linke_transposed.columns = table_data_linke_transposed.columns.astype(str)

# Erstellen der Tabelle für CDU/CSU
plt.figure(figsize=(10, 4))
plt.table(cellText=table_data_cdu_sorted.values, rowLabels=table_data_cdu_sorted.index, colLabels=table_data_cdu_sorted.columns, loc='center', bbox=[0.1,0.5,0.8,0.5])
plt.axis('off')
plt.title('Anzahl der Zwischenrufe von CDU/CSU pro Thema und Jahr\n')
plt.show()

# Erstellen der Tabelle für Die Linke
plt.figure(figsize=(10, 4))
plt.table(cellText=table_data_linke_sorted.values, rowLabels=table_data_linke_sorted.index, colLabels=table_data_linke_sorted.columns, loc='center', bbox=[0.1,0.5,0.8,0.5])
plt.axis('off')
plt.title('Anzahl der Zwischenrufe von Die Linke pro Thema und Jahr\n')
plt.show()
