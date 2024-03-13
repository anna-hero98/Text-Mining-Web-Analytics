import requests
import pandas as pd
import re
import subprocess

filepath = 'input_df_new_version.csv'
df = pd.read_csv(filepath, sep=';')
df.replace('\n', '', regex=True, inplace=True)
extracted_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

rede = ""

# Pro Zeile in Input_Df Rede auslesen
for jahr, dokumentnr, name, partei, thema, titel in zip(df['Jahr'], df['Dokumentnr'], df['Name'], df['Partei'],
                                                            df['Thema'], df['Titel']):

    # API
    url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']
                # Mithilfe von Regex Text cleanen
                text = re.sub(r'–', '-', text)
                text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

                search_sentence = titel
                words = search_sentence.split()
                shortened_title = search_sentence

                if len(words) > 2:
                    shortened_title = " ".join(words[2:-1])

                # Sucht nach dem zweiten Vorkommen des Titels
                titel_index = text.find(shortened_title, text.find(shortened_title) + 1)
                # Extrahiert Text nach dem zweiten Vorkommen des Titels
                result = text[titel_index:].strip()
                # result in Sätze mithilfe von Regex aufteilen, (?=[A-Z]+\. -> Außname für Mr. Dr. M. etc.
                sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z]+\. )', result)

                # Um später den Text zeilenweise einzulesen
                result_new = '\n'.join(sentences)

                start = f"{name} ({partei}):"
                end = "):"

                if start in result_new:
                    start = f"{name} ({partei}):"

                    start_index = result_new.find(start, result_new.find(start))
                    start_index += len(start)

                elif start != result_new:
                    start = f"{name} \(.+\) \({partei}\):"  # Findet z.B. Hartwig Fischer (Göttingen) (CDU/CSU):
                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # match -> Liste, diese in string umwandeln

                    start_index = result_new.find(newstart, result_new.find(newstart))
                    start_index += len(newstart)

                else:
                    start = f"{name}.*:"
                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # match -> Liste, diese in string umwandeln

                    start_index = result_new.find(start, result_new.find(start))
                    start_index += len(newstart)

                end_position = result_new.find(end, start_index)
                if end != -1:
                    rede = result_new[start_index:end_position].strip()
                    rede = rede.replace(';', r'')  # Nimmt Semikolon raus, damit es nicht zu Konflikten mit dem sep=";" kommt
                    break

        extracted_df = extracted_df._append(
                     {'Jahr': jahr, 'Dokumentnr': dokumentnr, 'Name': name, 'Partei': partei, 'Thema': thema,
                        'Titel': titel, 'Text': rede}, ignore_index=True)

    else:
        print("Error fetching data for dokumentnr:", dokumentnr)
extracted_df.to_csv('extracted_data.csv', sep = ";", index=False)

csv_file = 'extracted_data.csv'

# Öffnet die CSV-Datei im Betriebssystems
subprocess.Popen(['start', csv_file], shell=True)

