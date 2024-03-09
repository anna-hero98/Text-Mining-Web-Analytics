import collections
import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Laden des deutschen NLP-Modells
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 5000000

# Laden der CSV-Datei
data = pd.read_csv("extracted_data.csv").head(n=600).dropna()


# Alle Texte aus der Spalte "Text" zu einem einzigen Text zusammenführen
#oder weitere Bedingungen einfügen
text = " ".join(data['Text'])

# spaCy-Verarbeitung
doc = nlp(text)

# Lemmatisierung und Frequenzzählung
lemmas = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
lemma = collections.Counter(lemmas)
lemma_freq = Counter(lemmas)

wc = WordCloud().generate_from_frequencies(lemma_freq)
plt.imshow(wc)
plt.show()

# Sortieren der Frequenzen in absteigender Reihenfolge
for lemma, freq in lemma_freq.most_common():
    print(f"{lemma}: {freq}")
else:
    print("Keine Dokumente gefunden.")

