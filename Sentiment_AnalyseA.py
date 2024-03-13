import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv").head(n=600).dropna()

print(data)

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
            list_Sentimentwords.append((row['Thema'], row['Titel'], row['Jahr'], einzelnes_wort, wert, Cluster, sentence_with_word))

# DataFrame aus der Liste erstellen
df_Sentimentwords = pd.DataFrame(list_Sentimentwords, columns=['Thema', 'Titel', 'Jahr', 'Wort', 'Wert', 'Cluster', 'Satz'])

# Die Anzahl der gleichen Wörter zählen und in einer neuen Spalte hinzufügen
df_Sentimentwords['Anzahl'] = df_Sentimentwords.groupby(['Thema', 'Jahr', 'Cluster'])['Wert'].transform('count')

# Duplikate entfernen
df_Sentimentwords = df_Sentimentwords.drop_duplicates()

# DataFrame nach der Spalte "Anzahl" sortieren (absteigend)
df_Sentimentwords_sorted = df_Sentimentwords.sort_values(by='Anzahl', ascending=False)

print(df_Sentimentwords_sorted)

# DataFrame ohne das Wort "nan" erstellen
df_Sentimentwords_without_nan = df_Sentimentwords_sorted[df_Sentimentwords['Wort'] != 'nan']

# DataFrame nach Dokumentennummer gruppieren und Werte in der Spalte "Wert" aufsummieren
df_Sentimentwords_grouped = df_Sentimentwords_without_nan.groupby(['Jahr'])['Wert'].mean().reset_index()

# Visualisieren mit einem Liniendiagramm
plt.figure(figsize=(10, 6))
plt.plot(df_Sentimentwords_grouped['Jahr'], df_Sentimentwords_grouped['Wert'], marker='o')
plt.xlabel('Jahr')
plt.ylabel('Mittlere Werte')
plt.title('Sentiment-Analyse über die Jahre')
plt.grid(True)
plt.tight_layout()
plt.show()

# DataFrame nach Dokumentennummer gruppieren und Werte in der Spalte "Wert" aufsummieren
df_Sentimentwords_grouped = df_Sentimentwords_without_nan.groupby(['Thema', 'Jahr'])['Wert'].mean().reset_index()

# Visualisieren mit einem Liniendiagramm
plt.figure(figsize=(10, 6))
for theme, group in df_Sentimentwords_grouped.groupby('Thema'):
    plt.plot(group['Jahr'], group['Wert'], marker='o', label=theme)

plt.xlabel('Jahr')
plt.ylabel('Mittlere Werte')
plt.title('Sentiment-Analyse nach Thema über die Jahre')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gruppieren des DataFrames nach Thema und Auswahl der ersten 10 Wörter pro Thema
grouped_words = df_Sentimentwords_without_nan.groupby('Thema').head(100)

for theme, group in grouped_words.groupby('Thema'):
    # Filtere nur die Daten für die Jahre 2011-2016
    group_filtered = group[group['Jahr'].between(2011, 2016, inclusive='both')]

    words = group_filtered['Wort'].tolist()

    text = ' '.join(words)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'WordCloud für Thema: {theme} (2011-2016)')
    plt.axis('off')
    plt.show()

for theme, group in grouped_words.groupby('Thema'):
    # Filtere nur die Daten für die Jahre 2011-2016
    group_filtered = group[group['Jahr'].between(2018, 2023, inclusive='both')]

    words = group_filtered['Wort'].tolist()

    text = ' '.join(words)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'WordCloud für Thema: {theme} (2018-2023)')
    plt.axis('off')
    plt.show()
