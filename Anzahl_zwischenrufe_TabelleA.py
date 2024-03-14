import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Initialisierung der Zähler für Zwischenrufe pro Partei und Jahr
counter_per_party_year = {}

# Durchlaufen der Daten
for text, year, party in zip(data['Text'], data['Jahr'], data['Partei']):
    # Initialisierung des Zählers für die aktuelle Partei und das aktuelle Jahr
    if (party, year) not in counter_per_party_year:
        counter_per_party_year[(party, year)] = 0

    # Zwischenrufe für CDU/CSU zählen
    counter_per_party_year[(party, year)] += text.count("[CDU/CSU]:")

    # Zwischenrufe für Die Linke zählen
    counter_per_party_year[(party, year)] += text.count("[DIE LINKE]:")

# Konvertieren der aggregierten Daten in einen DataFrame
yearly_party_zwischenrufe_df = pd.DataFrame(list(counter_per_party_year.items()),
                                            columns=['Partei_Jahr', 'Anzahl_Zwischenrufe'])

# Aufteilen der kombinierten Spalte 'Partei_Jahr' in separate Spalten für Partei und Jahr
yearly_party_zwischenrufe_df[['Partei', 'Jahr']] = pd.DataFrame(yearly_party_zwischenrufe_df['Partei_Jahr'].tolist(),
                                                                index=yearly_party_zwischenrufe_df.index)

# Tabelle anzeigen
print(yearly_party_zwischenrufe_df)

# Daten für die Tabelle
table_data = yearly_party_zwischenrufe_df.pivot(index='Partei', columns='Jahr', values='Anzahl_Zwischenrufe')

# Erstellen der Tabelle
plt.figure(figsize=(10, 6))
plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center')

# Formatierung der Tabelle
plt.axis('off')
plt.title('Häufigkeit der Zwischenrufe pro Jahr und Partei')
plt.show()
