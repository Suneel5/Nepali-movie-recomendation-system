import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
url='https://en.wikipedia.org/wiki/List_of_Nepalese_films_of_2016'

response=requests.get(url)
# print(response.content)
# with open("output.html", "w", encoding="utf-8") as file:
#     file.write(response.text)
soup=BeautifulSoup(response.content,'html5lib')
tables=soup.find_all('table')
for (table_no,table) in enumerate(tables):
    if table_no ==11:
        break
    if table_no==0:
        headerrow=table.find_all('th')
        columns=[header.text.strip() for header in headerrow]
        df = pd.DataFrame(columns=columns[0:5])
        
    rows=table.find_all('tr')
  
    for row in rows:
        dictt={}
        vals=row.find_all('td')
        for i,val in enumerate(vals):
            if i<5:
                col_name=columns[i]
                dictt[col_name]=val.text.strip()

        new_row=pd.DataFrame(dictt, index=[0])
        df = pd.concat([df, new_row], ignore_index=True)

df.to_csv('data/2016_movies.csv')

                
            

