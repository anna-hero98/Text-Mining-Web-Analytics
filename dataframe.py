import match
import requests
import pandas as pd

file_path = 'Erster_Teil_Reden.csv'
df = pd.read_csv(file_path, sep=';')

extracted_df = pd.DataFrame(columns=['Dokumentnr', 'Text'])

for dokumentnr in df['Dokumentnr']:
    print("Fetching data for dokumentnr:", dokumentnr)

    api_url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']
                #match.re.search(r'E')
                extracted_df = extracted_df._append({'Dokumentnr': dokumentnr, 'Text': text}, ignore_index=True)
    else:
        print("Error fetching data for dokumentnr:", dokumentnr)

print(extracted_df.head())



"""
import requests
import pandas as pd
#import text_import_text

file_path = 'Erster_Teil_Reden.csv'
df = pd.read_csv(file_path, sep =';')
print(df.head())
extracted_df = pd.DataFrame(columns=['Dokumentnr', 'Text'])
for dokumentnr in df['Dokumentnr']:
    print(dokumentnr)

    api_url=f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

    response = requests.get(api_url, headers=headers)

    json_data = response.json()
    print(json_data)
    if 'documents' in json_data:
        # Iterate over each document
        for document in json_data['documents']:
            # Access the 'text' field for each document
            text = document['text']
            # for line in text:
            # if "" in line:
            extracted_df.append('Dokumentnr': dokumentnr, 'Text': text)
            
            """

