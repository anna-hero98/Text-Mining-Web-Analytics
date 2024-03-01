import requests
import pandas as pd
import re

# parteien = {"(CDU/CSU):","(DIE LINKE):","(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"}

filepath = 'Beispielliste.csv'
df = pd.read_csv(filepath, sep=';')
extracted_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

for jahr, dokumentnr, name, partei, thema, titel in zip(df['Jahr'], df['Dokumentnr'], df['Name'], df['Partei'],
                                                        df['Thema'], df['Titel']):
    print("Fetching data for dokumentnr:", dokumentnr)

    # API
    url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']

                # Entferne Zeilenumbrüche und nicht-sichtbare Leerzeichen
                text = re.sub(r'\s+', ' ', text).strip()

                # Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
                search_sentence = titel

                """titel = search_sentence
                # Split the sentence into words
                words = titel.split()
                # Extract the first two words and the last word
                shortened_title = " ".join(words[2:-1])

                # Shorten the last word by 10 letters
                if len(words[-1]) > 10:
                    shortened_last_word = words[-1][:-10]
                    shortened_title += " " + shortened_last_word
                else:
                    # If the last word is already shorter than 10 letters, keep it unchanged
                    shortened_title += " " + words[-1]"""


                #start = f"{name} ({partei}):"
                start = f"{name} {partei}:"
                parteien = ["(DIE LINKE):", "(CDU/CSU):", "(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"]
                rede = ""

                # Suchen nach dem zweiten Vorkommen des Ausrufezeichens
                titel_index = text.find(search_sentence, text.find(search_sentence) + 1)
                # Extrahieren des Teils nach dem zweiten Vorkommen des Ausrufezeichens
                result = text[titel_index:].strip()

                start_index = result.find(start, result.find(start))

                start_index += len(start)

                for partei in parteien:
                    end_position = result.find(partei, start_index)
                    if end_position != -1:
                        rede = result[start_index:end_position].strip()
                        print(rede)
                        break


        extracted_df = extracted_df._append(
                    {'Jahr': jahr, 'Dokumentnr': dokumentnr, 'Name': name, 'Partei': partei, 'Thema': thema,
                     'Titel': titel, 'Text': rede}, ignore_index=True)
    else:
        print("Error fetching data for dokumentnr:", dokumentnr)
print(extracted_df.head())
