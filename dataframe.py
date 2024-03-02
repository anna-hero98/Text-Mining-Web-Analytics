import match
import requests
import pandas as pd

#We generate a dataframe that includes the data of the speeches to the topics we want to analyze and the politician (+ party) that held the speech
file_path = 'Erster_Teil_Reden.csv'
input_df = pd.read_csv(file_path, sep=';')

#We create a second dataframe where we will store the data from the API call and some identifiers from the input_df before
extracted_df = pd.DataFrame(columns=['Dokumentnr', 'Text'])

#We create a for loop and call the Bundestags API that gives us back the speeches we will analyse.
#The input as query parameter is the number (dokumentnr) of the Plenarprotokoll
for dokumentnr in input_df['Dokumentnr']:
    print("Fetching data for dokumentnr:", dokumentnr)

    api_url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer={dokumentnr}'
    headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}

    response = requests.get(api_url, headers=headers)
#We filter the API response for the text that part, since we don't need the other parts
    if response.status_code == 200:
        json_data = response.json()
        if 'documents' in json_data:
            for document in json_data['documents']:
                text = document['text']
#Since we don't need all parts of the text we filter for the speech of the politican (FDP/Linke) and title of the topic that was discussed (the search parameters are taken from the input_df

                #match.re.search(r'E')
#In the extracted dataframe we write the id, Dokumentnr (number of the plenarprotocol), the extracted text according to the condition above, the party of the person doing the speech, the year of the speech, the topic that was discussed (sustainability, pensions...)
                #extracted_df = extracted_df._append({'Dokumentnr': dokumentnr, 'Text': text}, ignore_index=True)
               # Locate the position of the politician's name in the text

                #speech_title = input_df['Dokumentnr'] == [dokumentnr]['Titel'].values[0]
                #title_position  = text.find(speech_title)


                politician_name = input_df[input_df['Dokumentnr'] == [dokumentnr]['Linke'].values[0]]
                politician_position = text.find(politician_name)

                # Extract the content after the politician's name if found
                if politician_position != -1:
                    extracted_text = text[politician_position + len(politician_name):]
                    # Add the extracted text to the extracted dataframe
                    extracted_df = extracted_df._append({'Dokumentnr': dokumentnr, 'Text': extracted_text},
                                                       ignore_index=True)
    else:
        print("Error fetching data for dokumentnr:", dokumentnr)

print(extracted_df.head())
excel_file_path = 'extracted_data.xlsx'

# Export extracted_df to Excel
extracted_df.to_excel(excel_file_path, index=False)


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

