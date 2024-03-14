import spacy
import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nlp = spacy.load("de_core_news_sm")

# sia ist ein Sentiment Intensity Analyzer Tool, das die Polarität des Sentiments (positiv, neutral, negativ) und die Intensität des Sentiments im Satz berechnet
sia = SentimentIntensityAnalyzer()

punkt_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

# Datenbasis-Reden laden
data = pd.read_csv("extracted_data_new_version.csv", sep=';')
# Abgrenzung vor/nach AfD
filtered_data_before = data[data['Jahr'] < 2017]
filtered_data_after = data[data['Jahr'] > 2017]

# CSV mit Kraftausdrücken laden und in Liste konvertieren
kraftausdruecke_data = pd.read_csv("Kraftausdruecke.csv", sep=';')
kraftausdruecke_basis = []
for row in kraftausdruecke_data['Kraftausdruecke']:
    kraftausdruecke_basis.append(row)  # 1, da Anfang in Zeile 2 nach Überschrift

def analyze_kraftausdruecke(filtered_data_year):
    kraftausdruecke_all = []

    for jahr, partei, thema, text in zip(filtered_data_year['Jahr'], filtered_data_year['Partei'], filtered_data_year['Thema'], filtered_data_year['Text']):
        if isinstance(text, str):
            # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
            for kraftausdruck in kraftausdruecke_basis:
                if kraftausdruck in text:
                    sentences = punkt_tokenizer.tokenize(text)
                    for sentence in sentences:
                        if f" {kraftausdruck} " in f" {sentence} ":
                            sentence_nlp = nlp(sentence)
                            sentiment_scores = sia.polarity_scores(sentence_nlp.text)
                            if sentiment_scores['neg'] > 0.2:
                                kraftausdruecke_all.append(kraftausdruck)

    return kraftausdruecke_all

def analyze_compound_sentiment(filtered_data, party):
    kraftausdruecke_all = []
    kraftausdruecke_compound = []

    filtered_data_party = filtered_data[filtered_data['Partei'] == party]

    for jahr, partei, thema, text in zip(filtered_data_party['Jahr'], filtered_data_party['Partei'], filtered_data_party['Thema'], filtered_data_party['Text']):
        if isinstance(text, str):
            # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
            for kraftausdruck in kraftausdruecke_basis:
                if kraftausdruck in text:
                    sentences = punkt_tokenizer.tokenize(text)
                    for sentence in sentences:
                        if f" {kraftausdruck} " in f" {sentence} ":
                            sentence_nlp = nlp(sentence)
                            sentiment_scores = sia.polarity_scores(sentence_nlp.text)
                            if sentiment_scores['neg'] > 0.2:
                                kraftausdruecke_all.append(kraftausdruck)
                                kraftausdruecke_compound.append(sentiment_scores['compound'])

    count_kraftausdruecke = len(kraftausdruecke_all)
    avg_compound_sentiment = sum(kraftausdruecke_compound) / len(kraftausdruecke_compound) if kraftausdruecke_compound else 0

    return count_kraftausdruecke, round(avg_compound_sentiment, 3)

def wordcloud_create(result, time, years):
    kraftausdruecke_text = ' '.join(result)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(kraftausdruecke_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'WordCloud der Kraftausdrücke {time} Eintritt der AfD ({years})')
    plt.axis('off')
    return(plt.show())

# Liste mit Kraftausdrücken vor AfD / nach AfD
result_before = analyze_kraftausdruecke(filtered_data_before)
print('Liste Kraftausdrücke vor AfD: ',result_before)
result_after = analyze_kraftausdruecke(filtered_data_after)
print('Liste Kraftausdrücke nach AfD: ',result_after)

# Wordcloud erstellen vorher/nachher
wordcloud_create(result_before, 'vor', '2011-2016')
wordcloud_create(result_after, 'nach','2018-2023')

amount_before_CDUCSU, compound_before_CDUCSU = analyze_compound_sentiment(filtered_data_before, 'CDU/CSU')
amount_before_LINKE, compound_before_LINKE =analyze_compound_sentiment(filtered_data_before, 'DIE LINKE')
amount_after_CDUCSU, compound_after_CDUCSU =analyze_compound_sentiment(filtered_data_after, 'CDU/CSU')
amount_after_LINKE, compound_after_LINKE =analyze_compound_sentiment(filtered_data_after, 'DIE LINKE')

# Tabellen erstellen vorher
data1 = [
    ['', 'CDU/CSU', 'DIE LINKE'],
    ['Amount Before', amount_before_CDUCSU, amount_before_LINKE],
    ['Compound Before', compound_before_CDUCSU, compound_before_LINKE]
]
colWidths = [0.15, 0.1, 0.1]
plt.figure(figsize=(10, 5))
plt.table(cellText=data1, loc='center',colWidths=colWidths)
plt.axis('off')
plt.title('Häufigkeit und Compound-Score der Kraftausdrücke pro Partei vor Eintritt der AfD', pad=2)
plt.show()

# Tabellen erstellen nachher
data2 = [
    ['', 'CDU/CSU', 'DIE LINKE'],
    ['Amount Before', amount_after_CDUCSU, amount_after_LINKE],
    ['Compound Before', compound_after_CDUCSU, compound_after_LINKE]
]
plt.figure(figsize=(10, 5))
plt.table(cellText=data2, loc='center',colWidths=colWidths)
plt.axis('off')
plt.title('Häufigkeit und Compound-Score der Kraftausdrücke pro Partei nach Eintritt der AfD', pad=5)
plt.show()
