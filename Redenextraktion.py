import requests
import pandas as pd
import re
import subprocess

# Der Input Dataframe mit manuell gesuchten Daten wird eingelesen und Zeilenumbrüche werden gegen Leerzeichen ausgetauscht
filepath = 'input_df_new_version.csv'
input_df = pd.read_csv(filepath, sep=';')
input_df.replace('\n', '', regex=True, inplace=True)

# Der Extracted_df, in dem das finales Ergebnis gespeichert wird, wird vorbereitet
extracted_df = pd.DataFrame(columns=['Jahr', 'Dokumentnr', 'Name', 'Partei', 'Thema', 'Titel', 'Text'])

# Rede wird initialisiert
rede = ""

# Pro Zeile in Input_Df Rede wird der Inhalt ausgelesen
for jahr, dokumentnr, name, partei, thema, titel in zip(input_df['Jahr'], input_df['Dokumentnr'], input_df['Name'],
                                                        input_df['Partei'],
                                                        input_df['Thema'], input_df['Titel']):

    # Der API-Call für die DIP Bundestags-API wird gemacht
    url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
    response = requests.get(url, headers=headers)

    # Sofern die Response erfolgreich zurückkommt, wird die JSON weiterverarbeitet und der 'text' Anteil,
    # der die Reden enthält, wird extrahiert
    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']
                # Mithilfe von Regex Text cleanen
                # Lange Bindestriche werden gegen kurze Bindestriche ausgetauscht
                text = re.sub(r'–', '-', text)
                # Zeilenumbrüche & Sonderzeichen werden entfernt
                text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

                # Der Titel aus dem Input_DF wird als Search sentence gespeichert, in Wörter aufgeteilt
                # und gekürzt, wenn er länger als 2 Wörter ist
                search_sentence = titel
                words = search_sentence.split()
                shortened_title = search_sentence

                if len(words) > 2:
                    shortened_title = " ".join(words[2:-1])

                # Sucht nach dem zweiten Vorkommen des Titels
                titel_index = text.find(shortened_title, text.find(shortened_title) + 1)
                # Extrahiert Text nach dem zweiten Vorkommen des Titels
                result = text[titel_index:].strip()
                # result in Sätze mithilfe von Regex aufteilen, (?=[A-Z]+\. -> Ausnahme für Mr. Dr. M. etc.
                sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z]+\. )', result)

                # Um später den Text zeilenweise einzulesen
                result_new = '\n'.join(sentences)

                # Der Start der Rede wird als der Name und die Partei aus dem Input DF festgelegt
                start = f"{name} ({partei}):"
                # Das Erkennen des Endes Rede wird auf "):" gesetzt
                end = "):"

                # Es werden verschiedene Kombinationen, um den Redner ab Themenstart zu finden.
                # Wenn der Redner gefunden wird, dann wird ein Index gelegt
                # Klassischer Fall: Redner und Partei in Klammern und :
                if start in result_new:
                    start = f"{name} ({partei}):"

                    start_index = result_new.find(start, result_new.find(start))
                    start_index += len(start)
                # Doppelter Name: Bei doppelten Namen wird der Redner, der Wohnort in Klammern,
                # die Partei in Klammern und ein : gesetzt
                # Das Wohnortthema wird über die Verwendung von Regex gelöst
                elif start != result_new:
                    start = f"{name} \(.+\) \({partei}\):"  # Findet z.B. Hartwig Fischer (Göttingen) (CDU/CSU):
                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # match -> Liste, diese in string umwandeln

                    start_index = result_new.find(newstart, result_new.find(newstart))
                    start_index += len(newstart)

                # Im Falle von z.B. Ministern wird der Name, der Titel und dann ein Doppelpunkt gesetzt
                else:
                    start = f"{name}.*:"
                    regex_match = re.compile(start)
                    match = re.findall((regex_match), result_new)
                    newstart = "".join(match)  # match -> Liste, diese in string umwandeln

                    start_index = result_new.find(start, result_new.find(start))
                    start_index += len(newstart)

                # Das Ende wird nach dem Start Index gesucht
                # Wenn es gefunden wurde, dann wird die Rede zwischen den Start index und der Endposition ausgeschnitten
                end_position = result_new.find(end, start_index)
                if end != -1:
                    rede = result_new[start_index:end_position].strip()
                    rede = rede.replace(';',
                                        r'')  # Nimmt Semikolon raus, damit es nicht zu Konflikten mit dem sep=";" kommt
                    break
        #Das Ergebnis wird im extracted_df gespeichert
        extracted_df = extracted_df._append(
            {'Jahr': jahr, 'Dokumentnr': dokumentnr, 'Name': name, 'Partei': partei, 'Thema': thema,
             'Titel': titel, 'Text': rede}, ignore_index=True)

    else:
        print("Error fetching data for dokumentnr:", dokumentnr)

#Der extrahierte DF wird als CSV gespeichert
extracted_df.to_csv('extracted_data.csv', sep=";", index=False)

csv_file = 'extracted_data.csv'

# Öffnet die CSV-Datei im Betriebssystems
subprocess.Popen(['start', csv_file], shell=True)
