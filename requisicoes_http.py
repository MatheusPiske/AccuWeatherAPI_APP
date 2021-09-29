# Fluxo de uma requisição HTTP: Cliente prepara a requisição HTTP, ela vai ser enviada ao servidor, este vai recebê-la e procurar os dados e por fim, enviar a resposta com os dados solicitados. 
# Instalação do módulo 'Requests';
# status_code = 200 = OK (REQUISIÇÃO BEM SUCEDIDA);
# 403 = Forbidden: informação protegida por senha, a qual não foi enviada ou foi enviada de forma errada; 
# 404 = Not Found: não encontrado;
# r.headers = informações sobre a requisição;
# r.text = retorna o html da página

import requests 
r = requests.get('http://www.google.com')
#print(r.status_code)
#print(r.headers['Date'])
print(r.text)