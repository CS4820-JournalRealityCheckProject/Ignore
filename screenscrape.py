import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

articleList = [['Oxford Journal', '10.1093/jigpal/jzy015'],
               ['Oxford Journal', '10.1111/j.1095-8339.2011.01155.x'], #Does not work with code
               ['Oxford Journal', '10.1111/bij.12521'],
               ['Science Direct', '10.1016/j.ijrmhm.2018.07.009'],
               ['Science Direct', '10.1016/j.burnso.2018.03.001'], #Open access
               ['Springer', '10.1007/s10059-013-0080-3'],
                  ]

def DOItoURL(doi):
    url = "http://dx.doi.org/" + doi
    r = requests.get(url, allow_redirects=False)
    return (r.headers['Location'])

def ScienceDirect(doi, key):
    parameters ={"APIKey" : key}
    r = requests.get("https://api.elsevier.com/content/article/doi/"+doi, params = parameters)

    print(r.url)
    root = ET.fromstring(r.text)
    for item in root.iter():
        if item.text == "FULL-TEXT":
            return True
    return False

def Springer(doi):
    url = 'https://link.springer.com/article/'+doi

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('div', {"id": "article_no_access_banner"}):
        return False
    return True

def Oxford(doi):
    url = DOItoURL(doi)

    #Lie about who we are to get access
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    for title in soup.find_all('title'):
        if 'OUP | Not Found' in title.text:
            return False
    if soup.find('div', {"class": "article-top-info-user-restricted-options"}):
        return False
    return True

keySD = open("ApiKeys/ScienceDirect.txt").read()

for article in articleList:
    if article[0] == 'Oxford Journal':
        result = Oxford(article[1])
    elif article[0] == 'Springer':
            result = Springer(article[1])
    elif article[0] == 'Science Direct':
            result = ScienceDirect(article[1], keySD)
    print(str(result)+": "+article[1])