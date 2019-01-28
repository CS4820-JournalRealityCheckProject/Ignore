import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

doiList = ['10.1016/j.ijrmhm.2018.07.009', '10.1016/j.burnso.2018.03.001']
#[0] Science direct
#[1] Science direct(Open Access)
springerDoi = '10.1007/s10059-013-0080-3'

def ScienceDirect(doi, key):
    parameters ={"APIKey" : key}
    r = requests.get("https://api.elsevier.com/content/article/doi/"+doi, params = parameters)
    #print(r.url)
    #print(r.text)

    root = ET.fromstring(r.text)
    for item in root.iter():
        if item.text == "FULL-TEXT":
            return True
    return False

def Springer(doi):
    url = 'https://link.springer.com/article/'+doi

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for header in soup.find_all('div', {"id": "article_no_access_banner"}):
        return False
    return True

key = open("ApiKeys/ScienceDirect.txt").read()
#print(key)
for doi in doiList:
    result = ScienceDirect(doi, key)
    print ("("+str(result)+") "+doi)

result = Springer(springerDoi)
print ("("+str(result)+") "+springerDoi)