import requests
from bs4 import BeautifulSoup
deviceNumber='a0001'
url = 'http://127.0.0.1:8000/'+deviceNumber

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = str(BeautifulSoup(html, 'html.parser'))
    sentence=soup.split("{")
    max=len(sentence)-1
    sen=sentence[max]
    line=sen.split('"')
    mlx=line[9]
    lepton=line[13]
    print(mlx + " ," + lepton)

else :
    print(response.status_code)