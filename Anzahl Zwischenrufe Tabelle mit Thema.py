import pandas as pd
from matplotlib import pyplot as plt

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Initialisierung der Zähler für Zwischenrufe pro Partei, Jahr und Thema
counter_per_party_year_theme = {}

# Durchlaufen der Daten
for text, year, party, theme in zip(data['Text'], data['Jahr'], data['Partei'], data['Thema']):
    # Initialisierung des Zählers für die aktuelle Partei, das aktuelle Jahr und das aktuelle Thema
    if (party, year, theme) not in counter_per_party_year_theme:
        counter_per_party_year_theme[(party, year, theme)] = 0

    # Zwischenrufe für CDU/CSU zählen
    counter_per_party_year_theme[(party, year, theme)] += text.count("[CDU/CSU]:")

    # Zwischenrufe für Die Linke zählen
    counter_per_party_year_theme[(party, year, theme)] += text.count("[DIE LINKE]:")

# Konvertieren der aggregierten Daten in einen DataFrame
yearly_party_interruption_df = pd.DataFrame(list(counter_per_party_year_theme.items()), columns=['Partei_Jahr_Thema', 'Anzahl_Zwischenrufe'])

# Aufteilen der kombinierten Spalte 'Partei_Jahr_Thema' in separate Spalten für Partei, Jahr und Thema
yearly_party_interruption_df[['Partei', 'Jahr', 'Thema']] = pd.DataFrame(yearly_party_interruption_df['Partei_Jahr_Thema'].tolist(), index=yearly_party_interruption_df.index)

# Tabelle anzeigen
print(yearly_party_interruption_df)

# Daten für die Tabelle
table_data = yearly_party_interruption_df.pivot(index=['Partei', 'Thema'], columns='Jahr', values='Anzahl_Zwischenrufe')

# Erstellen der Tabelle
plt.figure(figsize=(12, 6))
table = plt.table(cellText=table_data.values, rowLabels=table_data.index, colLabels=table_data.columns, loc='center', cellLoc='center')

# Formatierung der Tabelle
plt.axis('off')

# Festlegen der Breite der Spalten
col_widths = [0.1] * len(table_data.columns)
#table.auto_set_column_width(col=list(range(len(table_data.columns))), widths=col_widths)

# Anpassen der Tabelle, um sie nach rechts zu verschieben
plt.subplots_adjust(left=0.4, bottom=0.1, top=0.9)

plt.title('Anzahl der Zwischenrufe pro Jahr, Partei und Thema')
plt.show()
