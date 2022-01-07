import requests
from bs4 import BeautifulSoup

def calibratedTemperature():
    deviceNumber='a0001'
    url='http://192.168.0.4:8000/'+deviceNumber

    response=requests.get(url)

    if response.status_code ==200:
        html=response.text
        soup=str(BeautifulSoup(html,"html.parser"))
        sentence=soup.split("{")
        max=len(sentence)-1
        sen=sentence[max]
        line=sen.split('"')
        mlx=line[9]
        lepton=line[13]
    else:
        print(response.status_code)

    return mlx,lepton

