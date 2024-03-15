import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Leere Datenstruktur erstellen für Zählen von Zwischenrufen pro Partei und Jahr
zäher_partei_jahr = {}

# Durchlaufen der Daten, Werte werden paarweise übermittelt
for text, year, party in zip(data['Text'], data['Jahr'], data['Partei']):
    # Initialisierung des Zählers für die aktuelle Partei und das aktuelle Jahr
    if (party, year) not in zäher_partei_jahr:
        zäher_partei_jahr[(party, year)] = 0

    # Zwischenrufe für CDU/CSU zählen
    zäher_partei_jahr[(party, year)] += text.count("[CDU/CSU]:")

    # Zwischenrufe für Die Linke zählen
    zäher_partei_jahr[(party, year)] += text.count("[DIE LINKE]:")

# Konvertieren der aggregierten Daten in einen DataFrame für Visualisierung
zwischenrufe_partei_jahr_df = pd.DataFrame(list(zäher_partei_jahr.items()),
                                            columns=['Partei_Jahr', 'Anzahl_Zwischenrufe'])

# Aufteilen der kombinierten Spalte 'Partei_Jahr' in separate Spalten für Partei und Jahr
zwischenrufe_partei_jahr_df[['Partei', 'Jahr']] = pd.DataFrame(zwischenrufe_partei_jahr_df['Partei_Jahr'].tolist(),
                                                                index=zwischenrufe_partei_jahr_df.index)

# Tabelle anzeigen
print(zwischenrufe_partei_jahr_df)

# Daten für die Tabelle
table_data = zwischenrufe_partei_jahr_df.pivot(index='Partei', columns='Jahr', values='Anzahl_Zwischenrufe')

# Erstellen der Tabelle
plt.figure(figsize=(10, 6))
plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center', bbox=[0.0,-1,1,1])

# Formatierung der Tabelle
plt.axis('off')
plt.title('Häufigkeit der Zwischenrufe pro Jahr und Partei')
plt.subplots_adjust(top=0.92) #Tabelle nach oben verschieben
plt.tight_layout() #Abstand der Tabelle und der Überschrift verringern
plt.show()
