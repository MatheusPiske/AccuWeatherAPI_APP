#import pprint
import json
import requests
from datetime import date
dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

accuweatherAPIKey = 'mWMdbkTRJ4sMaEceoIHvQkdi6EBypafZ'
mapboxAPIKey = 'pk.eyJ1IjoiYmFkZW96YW8iLCJhIjoiY2txMWg5N2kzMGVudDJ2cWJldmR0eWs1YiJ9.AfGG54bHjDQ4ZLlsVD_clw'
dias_semana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

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

def pegarPrevisao5Dias(codigoLocal):
    DailyAPIUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
       + codigoLocal + "?apikey=" + accuweatherAPIKey \
       + "&metric=true&language=pt-br&details=true&getphotos=false"
    r = requests.get(DailyAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter a previsão para os próximos dias.')
        return None
    else:
        try:
            DailyResponse = json.loads(r.text)
            infoClima5Dias = []
            for dia in DailyResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['Maximum']['Value']
                climaDia['min'] = dia['Temperature']['Minimum']['Value']
                climaDia['clima'] = dia['Day']['IconPhrase']
                diaSemana = date.fromtimestamp(dia['EpochDate']).strftime("%w")
                climaDia['dia'] = dias_semana[int(diaSemana)]
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            return None
 
def outrosLugares(): 
    local = input('Digite o nome do outro local: \n')
    mapboxGeoCodeUrl = 'https://api.mapbox.com/geocoding/v5/mapbox.places/local%20' + local + '.json?access_token=' + mapboxAPIKey
    
    r = requests.get(mapboxGeoCodeUrl)
        
    if (r.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else: 
      try:  
        localizacao = json.loads(r.text)
        coordenadas = {}
        coordenadas['long'] = str(localizacao["features"][0]["geometry"]["coordinates"][0])
        coordenadas['lat'] = str(localizacao["features"][0]["geometry"]["coordinates"][1])
        return coordenadas
      except:
        return None

# INICIO DO PROGRAMA

try:
  coordenadas = pegarCoordenadas()
  local = pegarCodigoLocal(coordenadas['lat'],coordenadas['long'])
  climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
  
  print('Clima atual em: ' + climaAtual['nomeLocal'])
  print(climaAtual['textoClima'])
  print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')
  
  # DESAFIO 01
  
  response = str(input("\nDeseja ver a previsão para os próximos dias? (s ou n): \n")).lower()

  while response == 's':
    previsoes = pegarPrevisao5Dias(local['codigoLocal'])
    for dia in previsoes:
      print(dia['dia'])
      print('Mínima: ' + str(dia['min']) + '\xb0' + 'C')
      print('Máxima: ' + str(dia['max']) + '\xb0' + 'C')
      print('Clima: ' + dia['clima'])
      print('-----------------------------------')

      response = "n"

  # DESAFIO 02

  response2 = str(input("\nDeseja ver a previsão de mais algum local? (s ou n): \n")).lower()
      
  while response2 == 's':
        
    outrosLocais = outrosLugares()
    local = pegarCodigoLocal(outrosLocais['lat'],outrosLocais['long'])
    climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])

    print('Clima atual em: ' + climaAtual['nomeLocal'])
    print(climaAtual['textoClima'])
    print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C') 
            
    response3 = str(input("\nDeseja ver a previsão para os próximos dias? (s ou n): "))
    while response3 == 's':
      previsoes = pegarPrevisao5Dias(local['codigoLocal'])
      for dia in previsoes:
        print(dia['dia'])
        print('Mínima: ' + str(dia['min']) + '\xb0' + 'C')
        print('Máxima: ' + str(dia['max']) + '\xb0' + 'C')
        print('Clima: ' + dia['clima'])
        print('-----------------------------------')
        response3 = "n"

    response2 = str(input("\nDeseja ver a previsão de mais algum local? (s ou n): \n")).lower()

except:
  print('Erro ao processar a solicitação. Entre em contato com o suporte.')

# FIM DO PROGRAMA

print('\n')
print('Obrigado por usar o WeatherApp!')
input()
