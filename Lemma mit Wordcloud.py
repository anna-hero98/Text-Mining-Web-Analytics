# Dieses Skript zeigt die Häufigkeit der Lemmata von CDU/CSU und Linken auf im Zeitraum vor und nach 2017. Die Visualisierung wird über eine Wordcloud gemacht. 

import pandas as pd
import collections
import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 49027203

# Laden der CSV-Datei "extracted_data_new_version.csv" und der CSV-Datei "vornamen"
data = pd.read_csv("extracted_data_new_version.csv", sep=";")
vornamen = pd.read_csv("vornamen.csv")

# Erstellen einer Liste aus den Vornamen in der CSV-Datei
vornamen_liste = vornamen["vorname"].tolist()

# Filtern auf die Partei und die Zeit
cdu_vor_2017 = data[(data['Partei'] == "CDU/CSU") & (data['Jahr'] < 2017)]
cdu_nach_2017 = data[(data['Partei'] == "CDU/CSU") & (data['Jahr'] > 2017)]
linke_vor_2017 = data[(data['Partei'] == "DIE LINKE") & (data['Jahr'] < 2017)]
linke_nach_2017 = data[(data['Partei'] == "DIE LINKE") & (data['Jahr'] > 2017)]

# Funktion zur Erstellung von Word Clouds für gegebene Daten
def wordcloud_create(data, title):
    # Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
    text = " ".join(data['Text'])

    # spaCy-Verarbeitung
    doc = nlp(text)

    # Lemmatisierung und Frequenzzählung der Reden
    lemmas = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and token.text.lower() not in ["beifall", "ausschuss", "drucksache"] and token.text.lower() not in vornamen_liste]
    lemma_frequenz = Counter(lemmas)

    # Erstellen der Word Cloud nur wenn Lemmata gefunden wurden
    if lemma_frequenz:
        # Erstellen der Word Cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(lemma_frequenz)

        # Anzeigen der Word Cloud
        plt.title(title)
        plt.axis('off')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.show()

# Word Clouds für die verschiedenen Parteien und Zeiträume erstellen
wordcloud_create(cdu_vor_2017, 'Wortwahl der CDU/CSU vor Eintritt der AfD')
wordcloud_create(cdu_nach_2017, 'Wortwahl der CDU/CSU nach Eintritt der AfD')
wordcloud_create(linke_vor_2017, 'Wortwahl der LINKEN vor Eintritt der AfD')
wordcloud_create(linke_nach_2017, 'Wortwahl der LINKEN nach Eintritt der AfD')
