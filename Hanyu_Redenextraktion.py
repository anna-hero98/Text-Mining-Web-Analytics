import requests
import pandas as pd
import re
import subprocess


# parteien = {"(CDU/CSU):","(DIE LINKE):","(BÜNDNIS 90/DIE GRÜNEN):", "(SPD):", "(FDP):", "(AfD):"}
filepath = 'input_csv.csv'
df = pd.read_csv(filepath, sep=';')
#Zeilenumbrüche bei Titel rausfiltern
df.replace('\n', '', regex=True, inplace=True)
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
                # Ersetzt ' – ' mit ' - '
                text = re.sub(r'–', '-', text)
                # Entfernt Bindestrich nachdem ein Zeilenumbruch kommt
                text = re.sub(r'-\n\s*', '-', text)
                # Entfernt Zeilenumbrüche und nicht-sichtbare Leerzeichen
                text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

                # Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
                search_sentence = titel

                # Split the sentence into words
                words = search_sentence.split()
                # Extract the first two words and the last word
                shortened_title = " ".join(words[2:-1])
                print(shortened_title)

                # Shorten the last word by 10 letters
                if len(words[-1]) > 10:
                    shortened_last_word = words[-1][:-10]
                    shortened_title += " " + shortened_last_word
            else:
                # If the last word is already shorter than 10 letters, keep it unchanged
                shortened_title += " " + words[-1]

                # Suchen nach dem zweiten Vorkommen des Titels
                titel_index = text.find(shortened_title, text.find(shortened_title) + 1)
                # Extrahieren des Teils nach dem zweiten Vorkommen des Titels
                result = text[titel_index:].strip()
                # result in Sätze mithilfe von re aufteilen, (?=[A-Z]+\. -> Außname für Mr. Dr. M. etc.
                sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z]+\. )', result)

                # Add newline character after each sentence
                result_new = '\n'.join(sentences)


                ende = "):"
                rede = ""

                start = f"{name} ({partei}):"

                if start in result_new:
                    print("Name + Partei")
                    start = f"{name} ({partei}):"
                    print(start)
                    zwischenfrage = "Zwischenfrage"

                    # Suchen Sie nach dem ersten Vorkommen von "start"
                    start_index = result_new.find(start)

                    # Überprüfen Sie, ob "start" im Text gefunden wurde
                    if start_index != -1:
                        # Suchen Sie nach dem letzten Vorkommen von "Zwischenfrage" vor dem ersten Vorkommen von "start"
                        search_range = result_new[max(0, start_index - 30):start_index]
                        zwischenfrage_index = search_range.rfind(zwischenfrage)

                        # Suchen Sie nach dem zweiten Vorkommen von "start"
                        if zwischenfrage_index != -1:
                            start_index = result_new.find(start, start_index)

                elif start != result_new:
                    print("Name + Zusatz + Partei")
                    start = f"{name} \(.+\) \({partei}\):"  # Findet z.B. Hartwig Fischer (Göttingen) (CDU/CSU):

                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # re.findall Ergebnis -> Liste, diese in string umwandeln
                    #print(newstart)

                    start_index = result_new.find(newstart, result_new.find(newstart))
                    start_index += len(newstart)
                else:
                    print("Name")
                    start = f"{name}.*:"

                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # re.findall Ergebnis -> Liste, diese in string umwandeln
                    #print(newstart)

                    start_index = result_new.find(start, result_new.find(start))
                    start_index += len(newstart)



                end_position = result.find(ende, start_index)
                if ende != -1:
                    rede = result[start_index:end_position].strip()
                    # print(rede)
                    break

        extracted_df = extracted_df._append(
                    {'Jahr': jahr, 'Dokumentnr': dokumentnr, 'Name': name, 'Partei': partei, 'Thema': thema,
                        'Titel': titel, 'Text': rede}, ignore_index=True)

    else:
        print("Error fetching data for dokumentnr:", dokumentnr)
print(extracted_df)
extracted_df.to_csv('extracted_data.csv', index=False)

csv_file = 'extracted_data.csv'

# Öffne die CSV-Datei im Standardprogramm des Betriebssystems
subprocess.Popen(['start', csv_file], shell=True)

