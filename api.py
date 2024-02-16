# dieses Modul macht Python fähig requests an Endpunkte rauszuschicken und die Response zu empfangen
import requests

idProtocol = 908
headers = {'Accept': 'application/json', 'Authorization': 'ApiKey rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF'}
url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.id={idProtocol}'
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
