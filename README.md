Project:

Im folgenden Projekt werden Bundestagsreden eingelesen und auf sprachliche Auffälligkeiten analysiert, mit dem Ziel Reden der CDU/CSU und der Linken vor und nach Einzug der AFD in den Bundestag auf Unterschiede zu analysieren. 
Dafür sollte zuerst Redenextraktion.py laufen gelassen werden.
Danach können mit den übrigen Modulen die extrahierten Reden auf verschiedene sprachliche Auffälligkeiten analysiert.

Installationsanleitung:
Die Dateien aus der requirements.txt müssen installiert werden. 
Außerdem sollte mittels "python -m spacy download de_core_news_sm" das Paket installiert werden, welches die deutsche Sprache analysiert.



Pythonversion: 
3.12.1

Benutzte Bibliotheken:

match~=0.3.2

matplotlib~=3.8.3

nltk~=3.8.1

numpy==1.26.3

pandas==2.2.0

regex==2023.12.25

requests~=2.31.0

spacy~=3.7.4

wordcloud~=1.9.3

#from Zwischenrufe counter?

#from Lemma: collections import Counter
