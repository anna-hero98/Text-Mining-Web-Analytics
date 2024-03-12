import spacy
import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 500000

# Initialisieren des Sentiment Intensity Analyzers
sia = SentimentIntensityAnalyzer()

# Initialisieren des Punkt-Tokenizers von NLTK
punkt_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

# Laden der CSV-Datein
data = pd.read_csv("extracted_data_new_version.csv", sep=';')
kraftausdruecke_data = pd.read_csv("Kraftausdruecke.csv", sep=';')


# Für die Speicherung der Liste der Kraftausdrücke
kraftausdruecke_list = []

# Für die Speicherung der Indizes
idx_list = []

for row in kraftausdruecke_data['Kraftausdruecke']:
    kraftausdruecke_list.append(row)  # 1, da Anfang in Zeile 2 nach Überschrift
#print(kraftausdruecke_list)

anzahl_treffer = 0

for idx, (jahr, partei, thema, text) in enumerate(zip(data['Jahr'], data['Partei'], data['Thema'], data['Text'])):
    if isinstance(text, str):
        # Überprüfen, ob eines der Kraftausdrücke in der Zeile vorkommt
        for kraftausdruck in kraftausdruecke_list:
            if kraftausdruck in text:
                sentences = punkt_tokenizer.tokenize(text)
                print(f"**{kraftausdruck}** gefunden in Zeile: {idx}\n Jahr: {jahr} Partei: {partei}  Thema: {thema}")
                anzahl_treffer += 1
                idx_list.append(idx)
                for sentence in sentences:
                    #sent_nlp = nlp(sentence)
                    if kraftausdruck in sentence:
                        highlighted_sentence = sentence.replace(kraftausdruck, f"**{kraftausdruck}**")  # Wenn Karftausdruck im Text wird das Wort durch **word** ersetzt um es hervorzuheben
                        highlighted_sentence = highlighted_sentence, kraftausdruck
                        hs_nlp = nlp(highlighted_sentence[0])
                        sentiment_scores = sia.polarity_scores(hs_nlp.text)  # Wenn Kraftausdruck vorliegt, wird eine Sentiemntanaylse durchgeführt
                        # sia ist ein Sentiment Intensity Analyzer Tool, das die Polarität des Sentiments (positiv, neutral, negativ) und die Intensität des Sentiments im Satz berechnet
                        print(f"Satz: {hs_nlp.text}")
                        print(f"Sentiment-Scores: {sentiment_scores}")
                        print(f"Wort:{kraftausdruck}\n")
    else:
        print("Für text keinen str erkannt")



print(anzahl_treffer)
print(idx_list)