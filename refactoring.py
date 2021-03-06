#import pprint
import json
import requests 

accuweatherAPIKey = 'mWMdbkTRJ4sMaEceoIHvQkdi6EBypafZ'

def pegarCoordenadas(): 
    r = requests.get('http://www.geoplugin.net/json.gp')
        
    if (r.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else:
      try:
          localizacao = json.loads(r.text)
          coordenadas = {}
          coordenadas['lat'] = localizacao['geoplugin_latitude']
          coordenadas['long'] = localizacao['geoplugin_longitude']
          return coordenadas
      except:
          return None

def pegarCodigoLocal(lat, long):   
     locationAPIUrl = "http://dataservice.accuweather.com/" \
     + "locations/v1/cities/geoposition/" \
     + "search?apikey=" + accuweatherAPIKey \
     + "&q=" + lat + "%2C" + long + "&language=pt-br"

     r = requests.get(locationAPIUrl)
     
     if (r.status_code != 200):
       print('Não foi possível obter o código do local.')
       return None
     else:
       try:
          locationResponse = json.loads(r.text)
          infoLocal = {}
          infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + ", " \
            + locationResponse['AdministrativeArea']['LocalizedName'] + ". " \
            + locationResponse['Country']['LocalizedName']
          infoLocal['codigoLocal'] = locationResponse['Key']
          return infoLocal
       except:
           return None
 
def pegarTempoAgora(codigoLocal, nomeLocal):       

       
    CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" \
        + codigoLocal + "?apikey=" + accuweatherAPIKey \
        + "&language=pt-br"

    r = requests.get(CurrentConditionsAPIUrl)
    if (r.status_code != 200):
       print('Não foi possível obter as condições do local.')
       return None
    else:
      try:
          CurrentConditionsResponse = json.loads(r.text)
          infoClima = {}
          infoClima['textoClima'] = CurrentConditionsResponse[0]['WeatherText']
          infoClima['temperatura'] = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
          infoClima['nomeLocal'] = nomeLocal
          return infoClima
      except:
          return None

#INICIO DO PROGRAMA

try:
  coordenadas = pegarCoordenadas()
  local = pegarCodigoLocal(coordenadas['lat'],coordenadas['long'])
  climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
  print('Clima atual em: ' + climaAtual['nomeLocal'])
  print(climaAtual['textoClima'])
  print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')
except:
  print('Erro ao processar a solicitação. Entre em contato com o suporte.')

input()
