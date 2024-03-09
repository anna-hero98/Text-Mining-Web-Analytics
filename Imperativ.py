import requests
import spacy
import pandas as pd

from collections import Counter
# Laden des deutschen Sprachmodells
nlp = spacy.load("de_core_news_sm")
#Erhöhung Anzahl an Zeichen
nlp.max_length = 5000000
# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv").head(n=600).dropna()


# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
#oder weitere Bedingungen einfügen
text = " ".join(data['Text'])

# spaCy-Verarbeitung
doc = nlp(text)



 # 1. Segmentierung des Textes in Sätze und Tokens
doc = nlp(text)
sentences = [sent.text.strip() for sent in doc.sents]

imperative_sentences = []

# 2. Anwenden des POS-Taggers und Identifizieren von Imperativsätzen
for sentence in sentences:
    sentence_doc = nlp(sentence)
    first_token_pos = sentence_doc[0].pos_
    last_token_text = sentence_doc[-1].text
    last_token_pos = sentence_doc[-1].pos_

    if (last_token_text.endswith('.') or last_token_text.endswith('!')) and first_token_pos == 'VERB':
        imperative_sentences.append(sentence)

# 3. Ausgabe der identifizierten Imperativsätze
if imperative_sentences:
    print("Identifizierte Imperativsätze:")
    for i, sentence in enumerate(imperative_sentences, 1):
        print(f"{i}. {sentence}")
    else:
        print("Keine Imperativsätze gefunden.")

else:
    print("Keine Dokumente gefunden.")