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

    def __repr__(self):
        print("Hello {}".format(self.tname))

    def __str__(self):
        print(self.tname)

session = requests.Session()
r = session.get('https://www.matchendirect.fr')

with open('tmp/matchlist', 'w') as fd:
    fd.write(r.text)


with open('tmp/matchlist') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

countrys = soup.find_all(class_='lienCompetition')
hours = soup.find_all(class_='lm1')
teams1 = soup.find_all(class_='lm3_eq1')
teams2 = soup.find_all(class_='lm3_eq2')



for country in countrys:
    r = session.get("https://www.matchendirect.fr/{}".format(country.a['href']))
    with open ('tmp/teamlist', 'w') as fd:
        fd.write(r.text)

    currentcountry = country.a.text.lower().split(' ')[0]
    print(currentcountry)

    with open('tmp/teamlist') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        teams = soup.find_all(class_='equipe')

    for team in teams:
        currentteam = team.text.lower()
        globals()[currentteam] = Team(currentcountry, currentteam)
        print(globals()[currentteam].__dict__)

