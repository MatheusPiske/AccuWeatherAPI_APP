import pprint
import json
import requests 
from time import sleep

accuweatherAPIKey = 'mWMdbkTRJ4sMaEceoIHvQkdi6EBypafZ'
r = requests.get('http://www.geoplugin.net/json.gp')
    
if (r.status_code != 200):
     print('Não foi possível obter a localização.')
else:
     localizacao = json.loads(r.text)
     latitude = localizacao['geoplugin_latitude']
     longitude = localizacao['geoplugin_longitude']
     
     locationAPIUrl = "http://dataservice.accuweather.com/" \
     + "locations/v1/cities/geoposition/" \
     + "search?apikey=" + accuweatherAPIKey \
     + "&q=" + latitude + "%2C" + longitude + "&language=pt-br"

     r2 = requests.get(locationAPIUrl)
     
     if (r.status_code != 200):
       print('Não foi possível obter o código do local.')
     else:
       locationResponse = json.loads(r2.text)
       nomeLocal = locationResponse['LocalizedName'] + ", " \
         + locationResponse['AdministrativeArea']['LocalizedName'] + ". " \
         + locationResponse['Country']['LocalizedName']
       codigoLocal = locationResponse['Key']

       print(f'Obtendo clima do local: {nomeLocal}')
       sleep(3)

       CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" \
         + codigoLocal + "?apikey=" + accuweatherAPIKey \
         + "&language=pt-br"

     r3 = requests.get(CurrentConditionsAPIUrl)
     if (r3.status_code != 200):
       print('Não foi possível obter as condições do local.')
     else:
       CurrentConditionsResponse = json.loads(r3.text)
       textoClima = CurrentConditionsResponse[0]['WeatherText']
       temperatura = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
       print(f'Clima no momento: {textoClima}')
       print(f'Temperatura: {temperatura} graus Celsius.')



input()
