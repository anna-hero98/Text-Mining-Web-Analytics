import requests
import pandas as pd

# API

headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

extracted_df = pd.DataFrame(columns=['Dokumentnr', 'Text'])

dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    json_data = response.json()

    for document in json_data['documents']:
        text = document['text']
        extracted_df = extracted_df._append({'Dokumentnr': dokumentnr, 'Text': text}, ignore_index=True)

    print("Data fetched successfully for dokumentnr:", dokumentnr)
    print(extracted_df.head())

else:
    print("Error fetching data for dokumentnr:", dokumentnr)

# Sentiment Analyse

# Importieren der Wortlisten
Path_positive = r"C:\Users\tobja\Downloads\SentiWS_v2.0\SentiWS_v2.0_Positive.txt"
Path_negative = r"C:\Users\tobja\Downloads\SentiWS_v2.0\SentiWS_v2.0_Negative.txt"

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
for index, row in extracted_df.iterrows():
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

output_file_path = r"C:\Users\tobja\Downloads\Sentimentwords_sorted.txt"
df_Sentimentwords_sorted.to_csv(output_file_path, sep='\t', index=False)

print(f"Der DataFrame wurde erfolgreich als Textdatei unter '{output_file_path}' gespeichert.")

# DataFrame nach Dokumentennummer gruppieren und Werte in der Spalte "Wert" aufsummieren
df_Sentimentwords_grouped = df_Sentimentwords_sorted.groupby('Dokumentnr')['Wert'].sum().reset_index()

print(df_Sentimentwords_grouped)