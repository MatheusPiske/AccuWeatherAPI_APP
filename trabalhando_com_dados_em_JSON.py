# JSON =  JavaScript Object Notation: Dicionário ou lista convertido para 'str';
# Uso do 'pprint' para enxergar melhor o dicionáriom json.loads(r.text)

import pprint
import json
import requests 

r = requests.get('http://www.geoplugin.net/json.gp')
    
if (r.status_code != 200):
     print('Não foi possível obter a localização.')
else:
     localizacao = json.loads(r.text)
     latitude = localizacao['geoplugin_latitude']
     longitude = localizacao['geoplugin_longitude']
     print(f'Latitude: {latitude}')
     print(f'Longitude: {longitude}')

input()
