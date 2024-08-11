import csv
import requests
from bs4 import BeautifulSoup

#Romance movie list, for search keyword "love"
romance = []
url="https://imsdb.com/genre/Romance"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('p > a')
tmp = [link['href'] for link in links]
romance.extend(tmp)


for i in range(0,len(romance)):
    tmp=romance[i][15:]
    movie_name=tmp[:-12]
    romance[i]=movie_name

print(romance)


#Science-Fiction movie list, for search keyword "science"
scifi = []
url="https://imsdb.com/genre/Sci-Fi"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('p > a')
tmp = [link['href'] for link in links]
scifi.extend(tmp)

for i in range(0,len(scifi)):
    tmp=scifi[i][15:]
    movie_name=tmp[:-12]
    scifi[i]=movie_name

print(scifi)


#Fantasy movie list, for search keyword "family"
family = []
url="https://imsdb.com/genre/Family"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('p > a')
tmp = [link['href'] for link in links]
family.extend(tmp)

for i in range(0,len(family)):
    tmp=family[i][15:]
    movie_name=tmp[:-12]
    family[i]=movie_name

print(family)

