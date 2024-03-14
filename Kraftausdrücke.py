import spacy
import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nlp = spacy.load("de_core_news_sm")
nlp.max_length = 500000

sia = SentimentIntensityAnalyzer()

punkt_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

data = pd.read_csv("extracted_data_new_version.csv", sep=';')
filtered_data_before = data[data['Jahr'] < 2017]
filtered_data_after = data[data['Jahr'] > 2017]

kraftausdruecke_data = pd.read_csv("Kraftausdruecke.csv", sep=';')
kraftausdruecke_list = []
for row in kraftausdruecke_data['Kraftausdruecke']:
    kraftausdruecke_list.append(row)  # 1, da Anfang in Zeile 2 nach Überschrift

kraftausdruecke_before_afd =[]
kraftausdruecke_after_afd =[]
kraftausdruecke_compound = []

def analyze_sentiment(filtered_data, kraftausdruecke_x_afd, neg_threshold=0.2):
    kraftausdruecke_x_afd = []

    for idx, (jahr, partei, thema, text) in enumerate(zip(filtered_data['Jahr'], filtered_data['Partei'], filtered_data['Thema'], filtered_data['Text'])):
        if isinstance(text, str):
            # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
            for kraftausdruck in kraftausdruecke_list:
                if kraftausdruck in text:
                    sentences = punkt_tokenizer.tokenize(text)
                    for sentence in sentences:
                        if f" {kraftausdruck} " in f" {sentence} ":
                            highlighted_sentence = sentence.replace(kraftausdruck, f"**{kraftausdruck}**")
                            hs_nlp = nlp(highlighted_sentence)
                            sentiment_scores = sia.polarity_scores(hs_nlp.text)
                            if sentiment_scores['neg'] > neg_threshold:
                                kraftausdruecke_x_afd.append(kraftausdruck)

    return kraftausdruecke_x_afd

result_before = analyze_sentiment(filtered_data_before, kraftausdruecke_before_afd, neg_threshold=0.2)
print('Liste Kraftausdrücke vor AfD: ',result_before)

result_after = analyze_sentiment(filtered_data_after, kraftausdruecke_after_afd, neg_threshold=0.2)
print('Liste Kraftausdrücke nach AfD: ',result_after)

def wordcloud_create(result, time, years):
    kraftausdruecke_text = ' '.join(result)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(kraftausdruecke_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'WordCloud der Kraftausdrücke {time} Eintritt der AfD ({years})')
    plt.axis('off')
    return(plt.show())

wordcloud_create(result_before, 'vor', '2011-2016')

wordcloud_create(result_after, 'nach','2018-2023')