import re
import requests 
from bs4 import BeautifulSoup

headers = {'user-agent':'Mozilla/5.0'}

resposta = requests.get('https://www.gov.br/infraestrutura/pt-br/assuntos/transito/conteudo-Senatran/portarias-senatran', headers = headers)
texto_completo = resposta.content
texto_arrumado = BeautifulSoup(texto_completo, 'html.parser')
lista_portarias = texto_arrumado.find_all('div', {'property': 'rnews:articleBody'})

lista_links_portarias = []

for div in lista_portarias:
    links = div.find_all('a', href=True)
    for link in links:
        lista_links_portarias.append(link['href'])
lista_links_portarias[1:-1]

headers = {'user-agent': 'Mozilla/5.0'}
lista_pdf_links = []

for link in lista_links_portarias[1:-1]:
    resposta = requests.get(link, headers=headers)
    texto_completo = resposta.content
    texto_arrumado = BeautifulSoup(texto_completo, 'html.parser')
    lista_a = texto_arrumado.find_all('a', href=True)
    for a in lista_a:
        if a['href'].endswith('.pdf'):
            lista_pdf_links.append(a['href'])

headers = {'user-agent': 'Mozilla/5.0'}
lista_pdf_links = []

for link in lista_links_portarias[1:-1]:
    resposta = requests.get(link, headers=headers)
    texto_completo = resposta.content
    texto_arrumado = BeautifulSoup(texto_completo, 'html.parser')
    lista_a = texto_arrumado.find_all('a', href=True)
    for a in lista_a:
        if a['href'].endswith('.pdf'):
            lista_pdf_links.append(a['href'])

if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

for pdf_link in lista_pdf_links:
    pdf_filename = pdf_link.split('/')[-1]
    pdf_path = os.path.join('pdfs', pdf_filename)
    response = requests.get(pdf_link)
    with open(pdf_path, 'wb') as f:
        f.write(response.content)
