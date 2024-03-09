import requests
import pandas as pd
import re
import subprocess

def build_and_process_dataframe():

    filepath = 'input_df.csv'
    df = pd.read_csv(filepath, sep=';')
    #Zeilenumbrüche bei Titel rausfiltern
    df.replace('\n', '', regex=True, inplace=True)
    extracted_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

    bsp_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

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
                    #text = re.sub(r'-\n\s*', '-', text)
                    # Entfernt Zeilenumbrüche und nicht-sichtbare Leerzeichen
                    text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

                    suche ="Flexibilisierung des Übergangs vom Erwerbsleben in den Ruhestand und zur Stärkung von Prävention und Rehabilitation"
                    if suche in text:
                        print("gefunden")


                    # Gesuchte Wortreihenfolge und Text nachfolgend bis zu einer anderen Wortfolge
                    search_sentence = titel

                    # Split the sentence into words
                    words = search_sentence.split()

                    # Initialize shortened_title with the original search_sentence
                    shortened_title = search_sentence

                    if len(words) > 3:
                        # Extract the first two words and the last word
                        shortened_title = " ".join(words[2:-3])
                        print(shortened_title)


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

                        start_index = result_new.find(start, result_new.find(start))
                        start_index += len(start)

                    elif start != result_new:
                        print("Name + Zusatz + Partei")
                        start = "Egon Jüttner" #f"{name} \(.+\) \({partei}\):"  # Findet z.B. Hartwig Fischer (Göttingen) (CDU/CSU):

                        regex_match = re.compile(start)
                        match = re.findall((regex_match), result_new)
                        newstart = "".join(match)  # re.findall Ergebnis -> Liste, diese in string umwandeln
                        print(newstart)

                        start_index = result_new.find(newstart, result_new.find(newstart))
                        start_index += len(newstart)
                    else:
                        print("Name")
                        start = f"{name}.*:"


                        regex_match = re.compile(start)
                        match = re.findall((regex_match), result_new)
                        newstart = "".join(match)  # re.findall Ergebnis -> Liste, diese in string umwandeln
                        print(newstart)

                        start_index = result_new.find(start, result_new.find(start))
                        start_index += len(newstart)




                    end_position = result_new.find(ende, start_index)
                    if ende != -1:
                        rede = result_new[start_index:end_position].strip()
                        rede = rede.replace(';', r'')  #Nimmt Semikolon raus, damit es nicht zu Konflikten mit dem sep=";" kommt
                        break

            extracted_df = extracted_df._append(
                        {'Jahr': jahr, 'Dokumentnr': dokumentnr, 'Name': name, 'Partei': partei, 'Thema': thema,
                         'Titel': titel, 'Text': rede}, ignore_index=True)

        else:
            print("Error fetching data for dokumentnr:", dokumentnr)
    print(extracted_df)
    extracted_df.to_csv('extracted_data.csv', sep = "*", index=False)

    csv_file = 'extracted_data.csv'

    # Öffne die CSV-Datei im Standardprogramm des Betriebssystems
    subprocess.Popen(['start', csv_file], shell=True)

build_and_process_dataframe()
