import requests
import spacy
import pandas as pd

nlp = spacy.load("de_core_news_sm")

filepath = 'Beispielliste.csv'
df = pd.read_csv(filepath, sep=';')
extracted_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

for jahr, dokumentnr, name, partei, thema, titel in zip(df['Jahr'], df['Dokumentnr'], df['Name'], df['Partei'], df['Thema'], df['Titel']):
    print("Fetching data for dokumentnr:", dokumentnr)

    #API
    url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']

                nlp.max_length = 3000000
                doc = nlp(text)
                text = text.replace('\u00A0', ' ')

                # Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
                search_sentence = titel
                start = f"{name} ({partei}):"
                parteien = ["(CDU/CSU):","(DIE LINKE):","(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"]

                count_search_sentence = 0
                count_partei = 0
                rede = ""

                # Finden der Startposition der gesuchten Wortreihenfolge
                for sent in doc.sents:
                    if search_sentence in sent.text:
                        count_search_sentence += 1
                        if count_search_sentence == 2:
                            # Finden der Startposition der gesuchten Wortreihenfolge
                            start_position = text.find(start)
                            # -1 ist ein spezieller Wert für "nicht gefunden" oder "nicht vorhanden"
                            if start_position != -1:
                                # Wenn die gesuchte Wortreihenfolge gefunden wurde, dann Abgleich mit Parteien Liste
                                for partei in parteien:
                                    count_partei += 1
                                    if count_partei == 2:
                                        end_position = text.find(partei, start_position)
                                        if end_position != -1:
                                            # Wenn die nachfolgende Wortfolge gefunden wurde
                                            rede = text[start_position:end_position]
                                            print(rede)
                                            break
                                else:
                                    # Wenn die nachfolgende Wortfolge nicht gefunden wurde
                                    print("Die nachfolgende Wortfolge wurde nicht gefunden.")
                            else:
                                # Wenn die gesuchte Wortreihenfolge nicht gefunden wurde
                                print("Die gesuchte Wortreihenfolge wurde nicht gefunden.")

                extracted_df = extracted_df._append({'Jahr':jahr,'Dokumentnr':dokumentnr,'Name':name,'Partei':partei,'Thema':thema,'Titel':titel,'Text': rede}, ignore_index=True)
        else:
            print("Error fetching data for dokumentnr:", dokumentnr)
print(extracted_df.head())
