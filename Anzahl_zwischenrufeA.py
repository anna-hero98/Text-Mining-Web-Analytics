import spacy
from collections import Counter
import pandas as pd


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

# Separates Zählen für jede Wortart
nouns = Counter([token.text for token in doc if token.pos_ == "NOUN"])
verbs = Counter([token.text for token in doc if token.pos_ == "VERB"])
adjectives = Counter([token.text for token in doc if token.pos_ == "ADJ"])
adverbs = Counter([token.text for token in doc if token.pos_ == "ADV"])

# Ausgabe nach Wortart sortiert
print("Substantive:")
for word, freq in nouns.most_common():
    print(f"{word}: {freq}")
print("\nVerben:")
for word, freq in verbs.most_common():
    print(f"{word}: {freq}")

print("\nAdjektive:")
for word, freq in adjectives.most_common():
    print(f"{word}: {freq}")

print("\nAdverbien:")
for word, freq in adverbs.most_common():
    print(f"{word}: {freq}")

print(f"Anzahl der Substantive: {sum(nouns.values())}")
print(f"Anzahl der Verben: {sum(verbs.values())}")
print(f"Anzahl der Adjektive: {sum(adjectives.values())}")
print(f"Anzahl der Adverbien: {sum(adverbs.values())}")