import requests
from bs4 import BeautifulSoup
import pandas as pd 

no=0
while True:
    print(no)
    url=f'https://www.imdb.com/search/title/?title_type=feature&languages=ne&sort=year,asc&start=0&ref_=adv_nxt'


    response=requests.get(url)
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    soup=BeautifulSoup(response.text,'html5lib')

    movies=soup.find_all(class_='lister-item-content')
    columns=['Title','Year','Genre','Director','Cast','Movie_id']
    df=pd.DataFrame(columns=columns)
    for movie in movies:
        dictt={}
        
        movie_name=movie.find('a').text.strip()
        dictt[columns[0]]=movie_name

        movie_id=movie.find('a').get('href')

        year=movie.find(class_='lister-item-year text-muted unbold').text.strip()
        dictt[columns[1]]=year

        genre=''
        try:
            genre=movie.find(class_='genre').text.strip()
        except:
            pass
        dictt[columns[2]]=genre

        dir_cast=movie.find('p',class_='').text.strip()
        director_start = dir_cast.find("Director:") + len("Director:")
        stars_start = dir_cast.find("Stars:") + len("Stars:")
        
        director = dir_cast[director_start:stars_start-len("Stars:")].strip()
        stars = [star.strip() for star in dir_cast[stars_start:].split(',')]

        dictt[columns[3]]=director
        dictt[columns[4]]=stars
        dictt[columns[5]]=movie_id
        new_row=pd.DataFrame([dictt],)
        df = pd.concat([df, new_row], ignore_index=True)

df.to_csv('data/imdb_scraped.csv')

    
  




    
