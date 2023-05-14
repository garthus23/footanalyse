#!/usr/bin/env python3

import os
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, send_from_directory
  
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

    def url(self, url):
        self.url = url

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
teamdict = [] 

ind=0
for country in countrys:
    currentcountry = country.a.text.lower().split(' ')[0]
    if country.a['href'] in desiredcountrys:
        r = session.get("https://www.matchendirect.fr/{}".format(country.a['href']))
    else:
        continue


    soup = BeautifulSoup(r.content, 'html.parser')
    teams = soup.find_all(class_='equipe')

    for team in teams:
        currentteam = team.text.lower()[1:]
        teamdict.append(Team(currentcountry, currentteam))
        teamdict[ind].logo = team.img['src']
        teamdict[ind].url = team.a['href']
        ind += 1

#for value in teamdict:
#        print(value.__dict__)

with open("teaminfo.json", "w") as outfile:
    json.dump([ob.__dict__ for ob in teamdict], outfile, ensure_ascii=False,indent=4, sort_keys=False)


app = Flask(__name__)
  
@app.route("/")
def home():
    return render_template("index.html", teams1=teams1, teams2=teams2, zip=zip)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
