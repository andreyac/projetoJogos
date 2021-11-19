"""
Created on Thu Jun  3 19:57:06 2021

@author: Andrey Costa
"""

import pandas as pd
from selenium import webdriver as wd
from bs4 import BeautifulSoup
from datetime import datetime

driver = wd.Firefox(executable_path =r'C:\Users\Andrey Costa\Downloads\Webdriver\geckodriver.exe')

criticGrades = []
userGrades = []
names = []
dates = []
mainGenres = []
secGenres = []
nUserReviews = []
nCrReviews = []

link = 'https://www.metacritic.com/game/pc/days-gone'

def makeSoup(link):
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content,"lxml")
    driver.close()
    del(content)
    return soup

def getGrade(soup, notas):
    trSoup = soup
    newSoup = BeautifulSoup(str(trSoup.select('span[itemprop="ratingValue"]')),"lxml")
    criticGrades.append(int(newSoup.get_text()[1:3]))
    del(newSoup,trSoup)
    return criticGrades

def getName(soup, names):
    names.append(soup.title.get_text())
    return names

def getUserGrade(soup,userGrades):
    ugsoup = soup.findAll('div',{'class':"metascore_w user large game positive"}, "lxml")
    grade = float(ugsoup[0].get_text())
    userGrades.append(grade)
    del(ugsoup, grade)
    return userGrades

def getDate(soup, dates):
    dt = soup.findAll('span', 'data')
    dataSTR = dt[1].get_text()
    date = datetime.strptime(dataSTR, '%b %d, %Y')
    dates.append(date)
    del(dataSTR, date)
    return dates

def getMainGenre(soup, mainGenres):
    dt = soup.findAll('span', 'data')
    genre = dt[5].get_text()
    mainGenres.append(genre)
    del(genre, dt)
    return mainGenres

def getSecGenre(soup, secGenres):
    dt = soup.findAll('span', 'data')
    genre = dt[6].get_text()
    secGenres.append(genre)
    del(genre, dt)
    return secGenres

def getNUR(soup, nUserReviews):
    dt = soup.findAll('a')
    gradesSTR = dt[195].get_text()
    gradesList = [int(s) for s in gradesSTR if s.isdigit()]
    lenGL = len(gradesList)
    grades = 0
    for i in range(lenGL):
        grades += (gradesList[i])*(10**(lenGL-i-1))
    nUserReviews.append(grades)
    del(dt, gradesSTR, gradesList, lenGL, grades)
    return nUserReviews

def getCUR(soup, nCrReviews):
    dt = soup.findAll('a')
    gradesSTR = dt[192].get_text()
    gradesList = [int(s) for s in gradesSTR if s.isdigit()]
    lenGL = len(gradesList)
    grades = 0
    for i in range(lenGL):
        grades += (gradesList[i])*(10**(lenGL-i-1))
    nCrReviews.append(grades)
    del(dt, gradesSTR, gradesList, lenGL, grades)
    return nCrReviews
    
soup = makeSoup(link)
getGrade(soup, criticGrades)
getName(soup, names)
getUserGrade(soup, userGrades)
getDate(soup, dates)
getMainGenre(soup, mainGenres)
getSecGenre(soup, secGenres)
getNUR(soup, nUserReviews)
getCUR(soup, nCrReviews)

data = {'nome' : names,
        'data lancamento' : dates, 
        'nota criticos' : criticGrades,
        'nota usuarios' : userGrades,
        'num. aval. usuarios' : nUserReviews,
        'num. aval. criticos' : nCrReviews,
        'generos primarios' : mainGenres,
        'generos secundarios' : secGenres}

df = pd.DataFrame(data)

df.to_csv('jogos.csv')
