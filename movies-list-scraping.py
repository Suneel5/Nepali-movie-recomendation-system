import requests
from bs4 import BeautifulSoup

url='https://en.wikipedia.org/wiki/List_of_Nepalese_films'

response=requests.get(url)
print(response)
print(response.status)
soup=BeautifulSoup(response.content,'html.praser')
