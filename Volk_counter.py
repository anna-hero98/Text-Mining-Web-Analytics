import collections
import pandas as pd
import spacy
from collections import Counter

# Laden des deutschen Sprachmodells von Spacy
nlp = spacy.load('de_core_news_sm')
nlp.max_length = 49027203

# Laden der CSV-Datei
data = pd.read_csv("extracted_data_new_version.csv", sep=";")

# Filtern auf die Partei
data_party_linke = data[(data['Partei'] == "DIE LINKE") & (data['Jahr'] > 2017)]

# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
text = " ".join(data_party_linke['Text'])

# spaCy-Verarbeitung
doc = nlp(text)

# Lemmatisierung und Frequenzzählung
lemmas = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and token.text.lower()]
lemma = collections.Counter(lemmas)
lemma_freq = Counter(lemmas)


# Sortieren der Frequenzen in absteigender Reihenfolge
for lemma, freq in lemma_freq.most_common():
    if lemma == "volk":
        print(f"{lemma}: {freq}")


