import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
url='https://en.wikipedia.org/wiki/List_of_Nepalese_films_of_2019'

response=requests.get(url)

# with open("output.html", "w", encoding="utf-8") as file:
#     file.write(response.text)
soup=BeautifulSoup(response.content,'html5lib')
tables=soup.find_all('table')
months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
for (table_no,table) in enumerate(tables):
    if table_no<2:
        if table_no==0:
            headerrow=table.find_all('th')
            columns=[header.text.strip() for header in headerrow]
            columns=columns[1:5]
            df = pd.DataFrame(columns=columns)
            
        rows=table.find_all('tr')

        for row in rows:
            dictt={}
            vals=row.find_all('td')

            index=0
            for i,val in enumerate(vals):
                if index<4:
                    value=val.text.strip()
                    if value.isdigit() or value in months:
                        continue


                    col_name=columns[index]
                    index+=1
                    dictt[col_name]=val.text

            new_row=pd.DataFrame(dictt, index=[0])
            df = pd.concat([df, new_row], ignore_index=True)

df.to_csv('data/2019_movies.csv')

                
            

