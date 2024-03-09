import requests
import pandas as pd

# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv").head(n=600).dropna()

# Sentiment Analyse

# Importieren der Wortlisten
Path_positive = r"SentiWS_v2.0_Positive.txt"
Path_negative = r"SentiWS_v2.0_Negative.txt"

# Wortlisten auslesen und in einer Tabelle speichern (Trennzeichen Tab)
lexikon_positive = pd.read_csv(Path_positive, sep='\t', header=None, names=['Wort', 'Wert', 'Synonym'])
lexikon_negative = pd.read_csv(Path_negative, sep='\t', header=None, names=['Wort', 'Wert', 'Synonym'])

# negative und positive Tabelle zusammenführen
Sentimentlexikon = pd.concat([lexikon_positive, lexikon_negative])

# Spalte Synonym als String formatieren (als Suchleiste  verwenden)
Sentimentlexikon['Synonym'] = Sentimentlexikon['Synonym'].astype(str)

print(Sentimentlexikon)

# eine Liste erstellen, die die Worte in einer Rede sucht
list_Sentimentwords = []
for index, row in data.iterrows():
    for einzelnes_wort in Sentimentlexikon['Synonym']:
        if einzelnes_wort in row['Text']:
            sentences = row['Text'].split('.')  # Annahme: Sätze werden durch Punkte getrennt
            sentence_with_word = next((s for s in sentences if einzelnes_wort in s), None)
            Cluster = Sentimentlexikon.loc[Sentimentlexikon['Synonym'] == einzelnes_wort, 'Wort'].values[0]
            wert = Sentimentlexikon.loc[Sentimentlexikon['Synonym'] == einzelnes_wort, 'Wert'].values[0]
            list_Sentimentwords.append((row['Dokumentnr'], einzelnes_wort, wert, Cluster, sentence_with_word))

# DataFrame aus der Liste erstellen
df_Sentimentwords = pd.DataFrame(list_Sentimentwords, columns=['Dokumentnr', 'Wort', 'Wert', 'Cluster', 'Satz'])

# Die Anzahl der gleichen Wörter zählen und in einer neuen Spalte hinzufügen
df_Sentimentwords['Anzahl'] = df_Sentimentwords.groupby(['Dokumentnr', 'Cluster'])['Wert'].transform('count')

# Duplikate entfernen
df_Sentimentwords = df_Sentimentwords.drop_duplicates()

# DataFrame nach der Spalte "Anzahl" sortieren (absteigend)
df_Sentimentwords_sorted = df_Sentimentwords.sort_values(by='Anzahl', ascending=False)

print(df_Sentimentwords_sorted)

df_Sentimentwords_sorted.to_csv('Sentimentwords_sorted.txt', sep='\t', index=False)

print(f"Der DataFrame wurde erfolgreich als Textdatei gespeichert.")

# DataFrame nach Dokumentennummer gruppieren und Werte in der Spalte "Wert" aufsummieren
df_Sentimentwords_grouped = df_Sentimentwords_sorted.groupby('Dokumentnr')['Wert'].sum().reset_index()

print(df_Sentimentwords_grouped)