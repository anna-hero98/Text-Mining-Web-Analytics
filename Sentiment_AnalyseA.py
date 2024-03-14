import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Laden der CSV-Datei mit den reden
data = pd.read_csv("extracted_data.csv").head(n=614).dropna()

# Importieren der Wortlisten
Path_positive = r"SentiWS_v2.0_Positive.txt"
Path_negative = r"SentiWS_v2.0_Negative.txt"

# Wortlisten auslesen und in einer Tabelle speichern (Trennzeichen Tab)
lexikon_positive = pd.read_csv(Path_positive, sep='\t', header=None, names=['Wort', 'Wert', 'Synonym'])
lexikon_negative = pd.read_csv(Path_negative, sep='\t', header=None, names=['Wort', 'Wert', 'Synonym'])

# negative und positive Tabelle zusammenführen
Sentimentlexikon = pd.concat([lexikon_positive, lexikon_negative])
Sentimentlexikon['Synonym'] = Sentimentlexikon['Synonym'].astype(str)

# eine Liste erstellen, die die Worte in einer Rede sucht
list_Sentimentwords = []
for index, row in data.iterrows():
    for einzelnes_wort in Sentimentlexikon['Synonym']:
        if einzelnes_wort in row['Text']:
            sentences = row['Text'].split('.')
            sentence_with_word = next((s for s in sentences if einzelnes_wort in s), None)
            Cluster = Sentimentlexikon.loc[Sentimentlexikon['Synonym'] == einzelnes_wort, 'Wort'].values[0]
            wert = Sentimentlexikon.loc[Sentimentlexikon['Synonym'] == einzelnes_wort, 'Wert'].values[0]
            list_Sentimentwords.append((row['Thema'], row['Titel'], row['Jahr'], row['Partei'], einzelnes_wort, wert,
                                        Cluster, sentence_with_word))

# DataFrame aus der Liste erstellen & aufbereiten
df_Sentimentwords = pd.DataFrame(list_Sentimentwords, columns=['Thema', 'Titel', 'Jahr', 'Partei', 'Wort', 'Wert', 'Cluster', 'Satz'])
df_Sentimentwords['Anzahl'] = df_Sentimentwords.groupby(['Thema', 'Jahr', 'Partei', 'Cluster'])['Wert'].transform('count')
df_Sentimentwords = df_Sentimentwords.drop_duplicates()
df_Sentimentwords_sorted = df_Sentimentwords.sort_values(by='Anzahl', ascending=False)
df_Sentimentwords_without_nan = df_Sentimentwords_sorted[df_Sentimentwords['Wort'] != 'nan']

# Datenaufbereitung inkl. Visualisieren mit Liniendiagrammen
df_Sentimentwords_grouped = df_Sentimentwords_without_nan.groupby(['Jahr', 'Partei'])['Wert'].mean().reset_index()

plt.figure(figsize=(10, 6))
for party, group in df_Sentimentwords_grouped.groupby('Partei'):
    plt.plot(group['Jahr'], group['Wert'], marker='o', label=party)

plt.xlabel('Jahr')
plt.ylabel('Mittlere Werte')
plt.title('Sentiment-Analyse über die Jahre')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

df_Sentimentwords_grouped = df_Sentimentwords_without_nan.groupby(['Jahr', 'Thema'])['Wert'].mean().reset_index()

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

# Datenaufbereitung inkl. Worclouds erstellen
grouped_words = df_Sentimentwords_without_nan.groupby('Thema').head(100)

for theme, group in grouped_words.groupby('Thema'):
    # Filtere nur für die Jahre 2011-2016
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
    # Filtere nur die Jahre 2018-2023
    group_filtered = group[group['Jahr'].between(2018, 2023, inclusive='both')]

    words = group_filtered['Wort'].tolist()

    text = ' '.join(words)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'WordCloud für Thema: {theme} (2018-2023)')
    plt.axis('off')
    plt.show()
