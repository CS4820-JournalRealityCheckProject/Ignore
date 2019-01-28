import requests
import xml.etree.ElementTree as ET
# from bs4 import BeautifulSoup

doiList = ['10.1016/j.ijrmhm.2018.07.009', '10.1016/j.burnso.2018.03.001']
#[0] Science direct
#[1] Science direct(Open Access)

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

key = open("ApiKeys/ScienceDirect.txt").read()
#print(key)
for doi in doiList:
    result = ScienceDirect(doi, key)
    print ("("+str(result)+") "+doi)