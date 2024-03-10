import requests
import spacy
from collections import Counter
import pandas as pd


# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 5000000

# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv").head(n=100).dropna()

# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
text = " ".join(data['Text'])

# Verarbeitung des Textes mit spaCy
doc = nlp(text)

# Identifizieren und Zählen von Superlativen
superlative_count = Counter()
for token in doc: #geht jedes Token in dem durch eine NLP-Bibliothek vorverarbeiteten Dokument doc durch (Basis/Idee VL Slides)
    if token.tag_ == "ADJA" and token.morph.get("Degree") == ["Sup"]:
    #Überprüfung, ob das aktuelle Token ein adj. Superlativ ist.
    #1. wird geprüft, ob der POS-Tag (Part-of-Speech Tag) des Tokens ADJA (ein Adjektiv )ist
    #2. wird überprüft, ob das morphologische Merkmal Degree des Tokens den Wert Sup hat
    # --> Bedeutet, dass das Adjektiv in der Superlativform vorliegt.
        superlative_count[token.text] += 1

# Ausgabe der Superlative und ihrer Häufigkeiten, absteigend sortiert
print("Superlativ - Häufigkeit")
for superlativ, haeufigkeit in superlative_count.most_common():
    print(f"{superlativ} - {haeufigkeit}")


## Visualiseurng der Ergebnisse --> Tabelle mit Anzahl. Zeitangabe (1x Tabelle: Vor AFD Eintritt)
## (1x Tabelle: Nach AFD Eintritt), mit Zeile pro Jahr + Häufigste Superlative auflisten



