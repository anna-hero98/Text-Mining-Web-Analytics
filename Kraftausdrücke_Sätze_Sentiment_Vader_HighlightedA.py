import spacy
import csv
import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 5000000

# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv",sep=';').head(n=10).dropna()


# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
#oder weitere Bedingungen einfügen
text = " ".join(data['Text'])

# spaCy-Verarbeitung
doc = nlp(text)

# Initialisieren des Sentiment Intensity Analyzers
sia = SentimentIntensityAnalyzer()

# Aufteilen des Textes in Sätze
sentences = list(doc.sents) #gibt einen Iterator über die Sätze des Dokuments zurück
#--> wird dann in eine Liste mit einzelnen Sätzen des Dokuments umgewandelt

#Lesen der Kraftausdrücke aus der CSV-Datei //
with open("Kraftausdruecke.csv") as kraftausdruecke_file: #With Block schließt am Ende Datei automatisch
    kraftausdruecke = [word[0] for word in csv.reader(kraftausdruecke_file)] #List comprehension
    #CSV wird zeileinweise gelesen --> Jede Zeile wird als Liste interpretiert
    #[word[0].....] ist eine List Comprehension, die durch jede Zeile der CSV iteriert
    #und das erste Element  (word[0]) jeder Zeile auswählt
    # --> Diese Elemente werden in einer neuen Liste "kraftausdruecke" gespeichert


    # Funktion, die prüft, ob und wo ein Kraftausdruck in einem Satz vorkommt
    def highlight_bad_words(sentence, kraftausdruecke):
        for word in kraftausdruecke:
            if word in sentence.text:
                # Hervorheben des Kraftausdrucks
                highlighted_sentence = sentence.text.replace(word, f"**{word}**") #Wenn Karftausdruck im Text wird das Wort durch **word** ersetzt um es hervorzuheben
                return highlighted_sentence, word #modifizierter Satz wird zurückgegeben
        return sentence.text, "null" #Wenn kein Kraftausdruck vorhanden, wird ursprünglicher Satz zurückgegeben

    # Durchführen der Sentimentanalyse für Sätze mit Kraftausdrücken
    for sentence in sentences:
        highlighted_sentence, word = highlight_bad_words(sentence, kraftausdruecke)
        if highlighted_sentence != sentence.text: #überprüft, ob der higl. Satz sich vom ursprünglich Satz unterscheidet --> Wenn Unterscheidung, dann liegt ein Kraftausdruck vor
            sentiment_scores = sia.polarity_scores(highlighted_sentence) #Wenn Kraftausdruck vorliegt, wird eine Sentiemntanaylse durchgeführt
            # sia ist ein Sentiment Intensity Analyzer Tool, das die Polarität des Sentiments (positiv, neutral, negativ) und die Intensität des Sentiments im Satz berechnet
            print(f"Satz: {highlighted_sentence}")
            print(f"Sentiment-Scores: {sentiment_scores}")
            print(f"Wort:{word}")
            #druckt die Sentiment-Scores --> Werte für die positiven, neutralen und negativen Aspekte des Sentiments sowie einen Gesamtwert
    else:
        print("Keine Dokumente gefunden.")


## Word cloud vor Einzug und nach Einzug (Wenn Kraftausdruck gefunden).
## Falls keine vorhanden, keine Visualisierung, da ziviler Umgang.

