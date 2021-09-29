#import pprint
import json
import requests
from datetime import datetime
dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

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
        infoLocal['nomeLocal'] = locationResponse['ParentCity']['LocalizedName'] + ", " \
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

def pegarPrevisao(codigoLocal):
    dailyForecastsAPIUrl = "http://dataservice.accuweather.com/forecasts/" \
    + "v1/daily/5day/" + codigoLocal + "?apikey=" + accuweatherAPIKey \
    + "&language=pt-br&metric=true"

    r = requests.get(dailyForecastsAPIUrl)
     
    if (r.status_code != 200):
      print('Não foi possível obter a previsão do local.')
      return None
    else:
        try:
          forecastResponse = json.loads(r.text)
          infoForecast = {}
          infoForecast['minima'] = str(forecastResponse['DailyForecasts'][0]['Temperature']['Minimum']['Value'])
          infoForecast['maxima'] = str(forecastResponse['DailyForecasts'][0]['Temperature']['Maximum']['Value'])
          infoForecast['clima'] = forecastResponse['DailyForecasts'][0]['Day']['IconPhrase']
          return infoForecast
        except:
          return None
 
         
#INICIO DO PROGRAMA


try:
  coordenadas = pegarCoordenadas()
  local = pegarCodigoLocal(coordenadas['lat'],coordenadas['long'])
  climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
  previsoes = pegarPrevisao(local['codigoLocal'])

  print('Clima atual em: ' + climaAtual['nomeLocal'])
  print(climaAtual['textoClima'])
  print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')
  
  #PREVISÕES(DESAFIO 01)
  
  dia = datetime.today().weekday()
  print("\n")
  print("Clima para hoje e para os próximos dias:")
  print("\n")
  print(dias_da_semana[dia])
  print('Mínima: ' + previsoes['minima'] + '\xb0' + 'C')
  print('Máxima: ' + previsoes['maxima'] + '\xb0' + 'C')
  print('Clima: ' + previsoes['clima'])
  print('-------------------------------------------')

except:
  print('Erro ao processar a solicitação. Entre em contato com o suporte.')


input()
