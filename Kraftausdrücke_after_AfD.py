import spacy
import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 500000

# Initialisieren des Sentiment Intensity Analyzers
sia = SentimentIntensityAnalyzer()

# Initialisieren des Punkt-Tokenizers von NLTK
punkt_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

# Laden der CSV-Datein
data = pd.read_csv("extracted_data_new_version.csv", sep=';')
filtered_data = data[data['Jahr'] > 2017]

kraftausdruecke_data = pd.read_csv("Kraftausdruecke.csv", sep=';')

# Für die Speicherung der Liste der Kraftausdrücke
kraftausdruecke_list = []

for row in kraftausdruecke_data['Kraftausdruecke']:
    kraftausdruecke_list.append(row)  # 1, da Anfang in Zeile 2 nach Überschrift

kraftausdruecke_after_afd=[]

for jahr, partei, thema, text in zip(filtered_data['Jahr'], filtered_data['Partei'], filtered_data['Thema'], filtered_data['Text']):
    if isinstance(text, str):
        # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
        for kraftausdruck in kraftausdruecke_list:
            if kraftausdruck in text:
                sentences = punkt_tokenizer.tokenize(text)
                for sentence in sentences:
                    if f" {kraftausdruck} " in f" {sentence} ":
                        highlighted_sentence = sentence.replace(kraftausdruck, f"**{kraftausdruck}**")  # Wenn Karftausdruck im Text wird das Wort durch **word** ersetzt um es hervorzuheben
                        highlighted_sentence = highlighted_sentence, kraftausdruck
                        hs_nlp = nlp(highlighted_sentence[0])
                        sentiment_scores = sia.polarity_scores(hs_nlp.text)  # Wenn Kraftausdruck vorliegt, wird eine Sentiemntanaylse durchgeführt
                        # sia ist ein Sentiment Intensity Analyzer Tool, das die Polarität des Sentiments (positiv, neutral, negativ) und die Intensität des Sentiments im Satz berechnet
                        if sentiment_scores['neg'] > 0.2:
                            kraftausdruecke_after_afd.append(kraftausdruck)


print(kraftausdruecke_after_afd)

# Wordcloud erstellen
kraftausdruecke_text = ' '.join(kraftausdruecke_after_afd)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(kraftausdruecke_text)

# Display the Wordcloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title(f'WordCloud der Kraftausdrücke nach Eintritt der AfD (2017-2023)')
plt.axis('off')
plt.show()