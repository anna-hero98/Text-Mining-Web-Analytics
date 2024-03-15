import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei "extracted_data_new_version.csv"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Leere Datenstruktur erstellen für Zählen von Zwischenrufen pro Partei, Jahr und Thema
zäher_partei_jahr_thema = {}

# Durchlaufen der Daten, Werte werden paarweise übermittelt
for text, year, party, theme in zip(data['Text'], data['Jahr'], data['Partei'], data['Thema']):
    # Initialisierung des Zählers für die aktuelle Partei, das aktuelle Jahr und das aktuelle Thema
    if (party, year, theme) not in zäher_partei_jahr_thema:
        zäher_partei_jahr_thema[(party, year, theme)] = 0

    # Zwischenrufe für CDU/CSU zählen
    zäher_partei_jahr_thema[(party, year, theme)] += text.count("[CDU/CSU]:")

    # Zwischenrufe für Die Linke zählen
    zäher_partei_jahr_thema[(party, year, theme)] += text.count("[DIE LINKE]:")

# Konvertieren der aggregierten Daten in einen DataFrame für Visualisierung
zwischenrufe_partei_jahr_thema_df = pd.DataFrame(list(zäher_partei_jahr_thema.items()), columns=['Partei_Jahr_Thema', 'Anzahl_Zwischenrufe'])

# Aufteilen der kombinierten Spalte 'Partei_Jahr_Thema' in separate Spalten für Partei, Jahr und Thema
zwischenrufe_partei_jahr_thema_df[['Partei', 'Jahr', 'Thema']] = pd.DataFrame(zwischenrufe_partei_jahr_thema_df['Partei_Jahr_Thema'].tolist(), index=zwischenrufe_partei_jahr_thema_df.index)

# Tabelle anzeigen
print(zwischenrufe_partei_jahr_thema_df)

# Daten für die Tabelle
table_data = zwischenrufe_partei_jahr_thema_df.pivot(index=['Partei', 'Thema'], columns='Jahr', values='Anzahl_Zwischenrufe')

# Erstellen der Tabelle
plt.figure(figsize=(12, 6))
table = plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center', cellLoc='center', bbox=[0.0,0.4,1,0.5])

# Formatierung der Tabelle
plt.axis('off')

# Festlegen der Breite der Spalten
col_widths = [0.1] * len(table_data.columns)

# Tabelle nadh rechts verschieben
plt.subplots_adjust(left=0.4, bottom=0.1, top=0.9)

plt.title('Anzahl der Zwischenrufe pro Jahr, Partei und Thema')
plt.show()
