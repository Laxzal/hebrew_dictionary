import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
url = 'https://www.pealim.com/dict/?'
limit = 'page='
page_number = 1

# Get page limit

response = requests.get(url + limit + str(page_number), headers={'User-Agent': user_agent})
print(response)
soup = BeautifulSoup(response.text, 'html.parser')
page_limit = soup.select('a[href*="?page="]')[-1].get('href')
page_limit = int(page_limit.replace('?page=', ''))

###Acquire word, root, part of speech and meaning
pealim_dataframe = pd.DataFrame(columns=['id', 'word','hebrew_pronunciation', 'root', 'part_of_speech', 'meaning', 'link'])

for page in range(page_number, page_limit+1):
    time.sleep(0.5)
    print(f'page number: {page} / {page_limit}')
    response = requests.get(url + limit + str(page), headers={'User-Agent': user_agent})
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.findAll('tr', {'onclick': True})

    for table_i in range(len(table)):
        hebrew_word = table[table_i].select('span[class*=menukad]')[0].text
        hebrew_pronunciation = table[table_i].select('span[class*=dict-transcription]')[0].text
        root = table[table_i].findAll('td')[1].text
        part_of_speech = table[table_i].findAll('td')[2].text
        meaning = table[table_i].findAll('td', {'class': 'dict-meaning'})[0].text
        link = table[table_i].findAll('a')[0].get('href')
        id_word = int(re.findall(r'(\d+)', table[table_i].findAll('a')[0].get('href'))[0])
        temp_array = np.array([id_word, hebrew_word,hebrew_pronunciation, root, part_of_speech, meaning, link]).reshape(1, -1)
        temp_df = pd.DataFrame(temp_array, columns=['id', 'word','hebrew_pronunciation', 'root', 'part_of_speech', 'meaning', 'link'])

        pealim_dataframe = pd.concat([pealim_dataframe, temp_df])

pealim_dataframe.to_csv('pealim_database.csv', index=False)
