#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup


class Country():
    def __init__(self, cname):
        self.cname = cname
    def __repr__(self):
        return "Hello"

    def __str__(self):
        return 'Hello'

class Team(Country):
    def __init__(self, cname, tname):
        self.tname = tname
        Country.__init__(self, cname)

    def logo(self, logo):
        self.logo = logo

    def __repr__(self):
        print("Hello {}".format(self.tname))

    def __str__(self):
        print(self.tname)

session = requests.Session()
r = session.get('https://www.matchendirect.fr')
soup = BeautifulSoup(r.content, 'html.parser')


countrys = soup.find_all(class_='lienCompetition')
hours = soup.find_all(class_='lm1')
teams1 = soup.find_all(class_='lm3_eq1')
teams2 = soup.find_all(class_='lm3_eq2')


desiredcountrys=['/france/ligue-1/','/france/ligue-2/','/allemagne/bundesliga-1/','/angleterre/barclays-premiership-premier-league/','/italie/serie-a/','/espagne/primera-division/']
teamdict = {}

for country in countrys:
    print(country)
    currentcountry = country.a.text.lower().split(' ')[0]
    if country.a['href'] in desiredcountrys:
        r = session.get("https://www.matchendirect.fr/{}".format(country.a['href']))
    else:
        continue


    soup = BeautifulSoup(r.content, 'html.parser')
    teams = soup.find_all(class_='equipe')

    for team in teams:
        currentteam = team.text.lower()[1:]
        teamdict[currentteam] = Team(currentcountry, currentteam)
        teamdict[currentteam].logo=team.img['src']

for key, value in teamdict.items():
        print(value.__dict__)
