import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url='https://juksun.com/nepali-movies/'

driver=webdriver.Chrome()
driver.get(url)
time.sleep(3)

while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'elementor-button-text'))
        )
        button.click()
        print('clicked')
        time.sleep(2)  # Wait for 2 seconds after clicking
    except Exception as e:
        print(f"Button is no longer available: {e}")
        break


time.sleep(10)
# driver.quit()

response=driver.page_source

driver.quit()
count=0
soup=BeautifulSoup(response,'html5lib')

all_movies_link=soup.find_all('a',class_='jet-listing-dynamic-image__link')
movies_link=[]
for link in all_movies_link:
        href = link.get('href')
        if href:
            movies_link.append(href)

# for movie_link in movies_link:

movielink=movies_link[1]
response=requests.get(movielink)
content = response.content.decode("utf-8")
with open("output.html", "w", encoding="utf-8") as file:
    file.write(content)

Film=soup.find('h1',class_='elementor-heading-title elementor-size-xl')
print(Film)# Film=Film[0].text
# print(Film.text)

actors=jet-listing-dynamic-field__content



     
     