# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 16:03:10 2021

@author: Andrey Costa
"""

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver as wd
from datetime import datetime

driver = wd.Firefox(executable_path =r'C:\Users\andre\Downloads\geckodriver.exe')

links = ['https://www.metacritic.com/browse/games/release-date/available/pc/date']
    
urlList = []
nomes = []
urls = []
datas = []
notaU = []
notaC = []

def makeSoup(link):
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content,'lxml')
    del(content)
    return soup

def scrapPages(link, nomes, urls, datas, notaU, notaC):
    soup = makeSoup(link)
    k = soup.findAll('a', href = True, class_='title')
    for i in range(len(k)):
        urls.append(k[i].get('href'))
        nomes.append(k[i].get_text())
        
    k = list(soup.findAll('div', href = False, class_='clamp-details'))
    for i in range(len(k)):
        k[i] = list(k[i])
        datas.append(k[i][3].get_text())

    k = list(soup.findAll('a', href = True, class_='metascore_anchor'))
    n = []
    i =  0
    while(i<100):
        n.append([list(k[i*3])[1],list(k[i*3+1])[1],list(k[i*3+2])[1]])
        i+=1
    k = n
    
    for i in range(len(k)):
        notaC.append(k[i][0].get_text())
        notaU.append(k[i][2].get_text())
    
    return nomes, urls, datas, notaU, notaC

def writeException(nomes,urls,datas,notaU,notaC):
    nomes.append('ERROR')
    urls.append('ERROR')
    datas.append('ERROR')
    notaU.append('ERROR')
    notaC.append('ERROR')
    return nomes,urls,datas,notaU,notaC
    
# def scrapLinks(link, urlList):
#     soup = makeSoup(link)
#     newSoup = BeautifulSoup(str(soup.findAll('tr')),'lxml')
#     urlSoup = newSoup.findAll('a', href=True, class_='title')
#     for el in urlSoup:
#         urlList.append('http://www.metacritic.com'+el['href'])
#     return urlList

soup = makeSoup(links[0])
soup1 = soup.findAll('a', href = True, class_='page_num')
last = int(soup1[len(soup1)-1].get_text())
for i in range(1,last+1):
    newlink = 'https://www.metacritic.com/browse/games/release-date/available/pc/date?page='+str(i)
    links.append(newlink)
del(soup,soup1,last,newlink)
    
for i in range(len(links)):
    try:
        scrapPages(links[i],nomes,urls,datas,notaU,notaC)
    except:
        writeException(nomes, urls, datas, notaU, notaC)


zipped = list(zip(nomes, urls, datas, notaU, notaC))
df = pd.DataFrame(zipped, columns=['Nome', 'URL','Lancamento', 'Av. Usuario', 'Av. Critica'])
dt = df[df['Av. Critica']!='ERROR']
df.to_csv('jogos.csv')
dt = dt[dt['Av. Critica']!='tbd']
dt.to_csv('jogosAVC.csv')
dt = dt[dt['Av. Usuario']!='tbd']
dt.to_csv('jogosAVUC.csv')
dt = df[df['Av. Usuario']!='tbd']
dt.to_csv('jogosACU.csv')

    