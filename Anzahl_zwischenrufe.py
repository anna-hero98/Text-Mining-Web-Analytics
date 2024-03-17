#Dieses Skript zählt die Zwischenrufe, die von der CDU/CSU und den Linken gemacht wurden. 
#Die Zwischenrufe werden dabei jeweils für den Zeitraum vor und nach 2017 betrachtet. Weiterhin werden die Ergebnisse in einer Tabelle visualisiert.
import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Initialisieren der Zähler pro Jahr
cdu_counts_per_year = {}
die_linke_counts_per_year = {}

# Durchlaufen der Daten aus der CSV
for text, year in zip(data['Text'], data['Jahr']):
    # Initialisieren der Zähler für das aktuelle Jahr
    if year not in cdu_counts_per_year:
        cdu_counts_per_year[year] = 0
    if year not in die_linke_counts_per_year:
        die_linke_counts_per_year[year] = 0

    # Zwischenrufe für CDU/CSU zählen
    cdu_counts_per_year[year] += text.count("[CDU/CSU]:")

    # Zwischenrufe für Die Linke zählen
    die_linke_counts_per_year[year] += text.count("[DIE LINKE]:")

# Erstellen eines DataFrames für die Anzeige der Ergebnisse in einer Tabelle
table_data = pd.DataFrame({'Jahr': list(cdu_counts_per_year.keys()),
                           'CDU/CSU': list(cdu_counts_per_year.values()),
                           'DIE LINKE': list(die_linke_counts_per_year.values())})

# Sortieren der Jahre aufsteigend
table_data = table_data.sort_values(by='Jahr')

# Setzen der Jahre als Index
table_data.set_index('Jahr', inplace=True)

# Anzeige der transponierten Tabelle
print(table_data)

# Erstellen und Formatieren der Tabelle
plt.figure(figsize=(10, 6))
plt.table(cellText=table_data.T.values, rowLabels=table_data.columns, colLabels=table_data.index, loc='center', bbox=[0.1,0.8,0.8,0.15])
plt.axis('off')
plt.title('Anzahl der Zwischenrufe von CDU/CSU und den linken pro Jahr\n')
plt.show()
