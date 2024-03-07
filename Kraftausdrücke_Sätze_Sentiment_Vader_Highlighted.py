import requests
import spacy
import csv
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 2027203

# Initialisieren des Sentiment Intensity Analyzers
sia = SentimentIntensityAnalyzer()

# Headers für die API-Anfrage
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

# Eingabe der Dokumentnummer
Dokumentnr = input('Bitte Dokumentnummer eingeben: ')
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={Dokumentnr}'
response = requests.get(url, headers=headers)

json_data = response.json()

if 'documents' in json_data:
    for document in json_data['documents']:
        text = document['text']

        # Aufteilen des Textes in Sätze
        doc = nlp(text)
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
                    return highlighted_sentence #modifizierter Satz wird zurückgegeben
            return sentence.text #Wenn kein Kraftausdruck vorhanden, wird ursprünglicher Satz zurückgegeben

        # Durchführen der Sentimentanalyse für Sätze mit Kraftausdrücken
        for sentence in sentences:
            highlighted_sentence = highlight_bad_words(sentence, kraftausdruecke)
            if highlighted_sentence != sentence.text: #überprüft, ob der higl. Satz sich vom ursprünglich Satz unterscheidet --> Wenn Unterscheidung, dann liegt ein Kraftausdruck vor
                sentiment_scores = sia.polarity_scores(highlighted_sentence) #Wenn Kraftausdruck vorliegt, wird eine Sentiemntanaylse durchgeführt
                # sia ist ein Sentiment Intensity Analyzer Tool, das die Polarität des Sentiments (positiv, neutral, negativ) und die Intensität des Sentiments im Satz berechnet
                print(f"Satz: {highlighted_sentence}")
                print(f"Sentiment-Scores: {sentiment_scores}")
                #druckt die Sentiment-Scores --> Werte für die positiven, neutralen und negativen Aspekte des Sentiments sowie einen Gesamtwert
else:
    print("Keine Dokumente gefunden.")


## Word cloud vor Einzug und nach Einzug (Wenn Kraftausdruck gefunden).
## Falls keine vorhanden, keine Visualisierung, da ziviler Umgang.

