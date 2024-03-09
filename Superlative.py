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

# spaCy-Verarbeitung
doc = nlp(text)

# Identifizieren und Zählen von Superlativen
superlative_count = Counter()
for token in doc:
    if token.tag_ == "ADJA" and token.morph.get("Degree") == ["Sup"]:
        superlative_count[token.text] += 1

# Ausgabe der Superlative und ihrer Häufigkeiten, absteigend sortiert
print("Superlativ - Häufigkeit")
for superlativ, haeufigkeit in superlative_count.most_common():
    print(f"{superlativ} - {haeufigkeit}")

