import requests
import os
from os import name, path, walk
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from datetime import datetime, date, time
import os
from os import walk
from instaloader import Instaloader, Profile
PATH_TO_PROJECT = '/home/thuy/Desktop/ML_project'
import sys
sys.path.append(PATH_TO_PROJECT)

__all__ = [
    'DowloadPage',
    'get'

]
class DowloadPage:
    def __init__(self,
    url_start="https://www.transfermarkt.com",
    urls=['/premier-league/startseite/wettbewerb/GB1',
    '/primera-division/startseite/wettbewerb/ES1',
    '/1-bundesliga/startseite/wettbewerb/L1',
    '/serie-a/startseite/wettbewerb/IT1',
    '/ligue-1/startseite/wettbewerb/FR1']):
        self.urls = urls
        self.url_start = url_start
    def dowload(self, dirtosave):
        os.makedirs(dirtosave, exist_ok=True)
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        count = 0
        count_err = 0
        for url in self.urls:
            count += 1
            try:
                url = url.strip()
                page = requests.get(self.url_start+url, headers=headers)
                with open(dirtosave+'/{}_{}.html'.format(url.split('/')[1], url.split('/')[-1]), 'w',
                encoding='utf-8') as fw:
                    fw.write(page.text)
            except:
                count_err += 1
                print('>> +1 err : row {}'.format(count))
                continue
        return '>>successfully, {}/{} writed into {}'.format(count-count_err, count, dirtosave)

class GetUrlTeams:
    def __init__(self):
        pass
    def read_url_teams(self, dirtoread):
        fileLst = next(walk(dirtoread), (None, None, []))[2]
        self.lstTeamUrl = []
        count = 0
        for file in fileLst:
            with open('{}/{}'.format(dirtoread, file), 'r',
                encoding='utf-8') as fr:
                page = fr.read()
            soup = BeautifulSoup(page, 'html.parser')
            for tag in soup.find_all('td', attrs = {'class' : 'hauptlink no-border-links hide-for-small hide-for-pad'}):
                self.lstTeamUrl.append(tag.a['href'])
                count += 1
        return '>>successfully, read {}'.format(count)
    def write_url_team(self, dirtowrite, filename):
        os.makedirs(dirtowrite, exist_ok=True)
        with open('{}/{}.txt'.format(dirtowrite, filename), 'w',
                encoding='utf-8') as fw:
            fw.write('\n'.join(self.lstTeamUrl))
        return '>>successfully, writed into {}/{}.txt'.format(dirtowrite, filename)
class GetUrlPlayers:
    def __init__(self) -> None:
        pass
    def read_url_players(self, dirtoread):
        fileLst = next(walk(dirtoread), (None, None, []))[2]
        self.lstUrlPlayers = []
        count = 0
        for file in fileLst:
            with open('{}/{}'.format(dirtoread, file), 'r',
                encoding='utf-8') as fr:
                page = fr.read()
            soup = BeautifulSoup(page, 'html.parser', multi_valued_attributes=None)
            for tag in soup.find_all('span', attrs = {'class' : 'hide-for-small'}):
                self.lstUrlPlayers.append(str(tag.a['href']))
                count += 1
        return '>>successfully, read {}'.format(count)
    def write_url_players(self, dirtowrite, filename):
        os.makedirs(dirtowrite, exist_ok=True)
        with open('{}/{}.txt'.format(dirtowrite, filename), 'w',
                encoding='utf-8') as fw:
            fw.write('\n'.join(self.lstUrlPlayers))
        return '>>successfully, writed into {}/{}.txt'.format(dirtowrite, filename)

class get_attr():
    def __init__(self, soup):
        self.soup = soup

    def get_name(self):
        name = ''
        try:
            for i in self.soup.find('h1', attrs = {'itemprop' : 'name'}).strings:
                name += (' '+ str(i).strip())
        except:
            name = ''
        return name.strip()

    def get_urlInsta(self):
        try:
            url = str(self.soup.find('div',attrs = 'socialmedia-icons').find_all('a', attrs = {'title' : 'Instagram'})[0]['href'])
        except:
            url = None
        return url

    def get_follower(self):
        url = self.get_urlInsta()
        if url == '':
            return None
        def get_nameIn(url):
            url = str(url)
            nameIn = url.split('.com/')[1].strip().split('/')[0]
            return nameIn.strip()
        try:
            prfiN = get_nameIn(url)
            L = Instaloader()
            profile = Profile.from_username(L.context, prfiN)
            followers = int(profile.followers)
        except:
            return None
        return followers/1000000
    def get_height(self):
        try:
            tag = self.soup.find('span', attrs = {'itemprop' : 'height'})
            tmp = str(tag.string).split(' ')[0].replace(',', '.').strip()
            height = float(tmp)
        except:
            height = None
        return height

    def get_age(self):
        try:
            tag = self.soup.find('span', string = 'Age:')
            mainTag = tag.find_next_sibling('span')
            age = int(mainTag.string)
        except:
            age = None
        return age

    def get_position(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = 'Position:')
            mainTag = tag.find_next_sibling('span')
            position = str(mainTag.string.strip().split(' ')[0])
        except:
            position = None
        return position
    def get_foot(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = 'Foot:')
            mainTag = tag.find_next_sibling('span')
            foot = str(mainTag.string)
        except:
            foot = None
        return foot

    def get_agent(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = 'Player agent:')
            mainTag = tag.find_next_sibling('span').a
            agent = str(mainTag.string)
        except:
            agent = None
        return agent

    def get_club(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = re.compile('Current club:'))
            mainTag = tag.find_next_sibling('span').a
            club = str(mainTag['title'])
        except:
            club = None
        return club

    def get_outfitter(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = 'Outfitter:')
            mainTag = tag.find_next_sibling('span')
            outfitter = str(mainTag.string)
        except:
            outfitter = None
        return outfitter

    def get_contract_expires(self):
        def get_contract_expires_2(soup):
            tag = soup.find('span', attrs = {'class' : re.compile('info-table')}, string = 'Contract expires:')
            mainTag = tag.find_next_sibling('span')
            tmp = str(mainTag.string)
            return tmp
        try:
            dt = datetime.strptime(get_contract_expires_2(self.soup), '%b %d, %Y')
        except:
            dt = None
        return dt

    def get_country(self):
        try:
            tag = self.soup.find('span', attrs = {'class' : re.compile('info-table')}, string = re.compile('Citizenship:'))
            mainTag = tag.find_next_sibling('span').img
            country = str(mainTag['title'])
        except:
            country = None
        return country
        
    def get_number(self):
        try:
            mainTag = self.soup.find('span', attrs = {'class' : 'dataRN'})
            tmp = str(mainTag.string).split('#')[1]
            num = int(tmp)
        except:
            num = None
        return num

    def get_price(self):
        count = 0
        try:
            for count, i in zip(range(0, 5), self.soup.find('div', attrs = {'class' : 'dataMarktwert'}).a.strings):
                if count == 1:
                    price = float(i)
                elif count == 2:
                    currency = str(i)
            if currency == 'Th.':
                price = price / 1000
            price = round(price, 3)
        except:
            price = None
        return price

    def get_league(self):
        try:
            for i in self.soup.find('span', attrs = {'class' : 'mediumpunkt'}).a.strings:
                league = str(i).strip()
        except:
            league = None
        return league

    def get_erfolge(self):
        count = 0 
        try:
            for i in list(self.soup.find('div', attrs = {'class' : 'dataErfolge hide-for-small'}).find_all('a')):
                try:
                    strTmp = str(i.span.string)
                    numTmp = int(strTmp)
                    count += numTmp
                except:
                    continue
        except:
            count = 0
        return count

    def get_capsgoals(self):
        try:
            dadTag = self.soup.find('span', string = 'Caps/Goals:').find_next_siblings('span')[0]
            tags = dadTag.find_all('a')
        except:
            return 0, 0
        if len(tags) < 2:
            return 0, 0
        try:
            caps = int(str(tags[0].string))
            goalsCap = int(str(tags[1].string))
        except:
            return 0, 0
        return caps, goalsCap
        
    def get_score(self):
        tmp = ''
        try: 
            for td in self.soup.find('td', string = re.compile('Total'), attrs = {'class' : re.compile('rechts hide')}).find_next_siblings('td', attrs = {'zentriert'}):
                possibleNull = str(td.string)
                if possibleNull == '-':
                    tmp = tmp + '0' + '/'
                    continue
                tmp = tmp + str(td.string) + '/'
        except:
            tmp = None
        return tmp
    
class GetDf:
    def __init__(self) -> None:
        pass
    def get_df(self, dirtoread):
        self.dirtoread = dirtoread
        fileLst = next(walk(self.dirtoread), (None, None, []))[2]
        self.count = 0
        self.count_err = 0
        lstmakedf = []
        for file in fileLst:
            try:
                self.count += 1
                with open('{}/{}'.format(self.dirtoread, file), 'r', 
                encoding='utf-8') as fr:
                    page = fr.read()
            except:
                print('\nnot such/open file')
                self.count_err += 1
                continue
            soup = BeautifulSoup(page, 'html.parser')
            playerDict = {}
            attrs = get_attr(soup)
            playerDict['name'] = attrs.get_name()
            playerDict['number'] = attrs.get_number()
            playerDict['league'] = attrs.get_league()
            playerDict['age'] = attrs.get_age()
            playerDict['height'] = attrs.get_height()
            playerDict['position'] = attrs.get_position()
            playerDict['erfolge'] = attrs.get_erfolge()
            playerDict['caps'], playerDict['goalsCap'] = attrs.get_capsgoals()
            playerDict['urlInsta'] = attrs.get_urlInsta()
            playerDict['follower'] = attrs.get_follower()
            playerDict['foot'] = attrs.get_foot()
            playerDict['agent'] = attrs.get_agent()
            playerDict['club'] = attrs.get_club()
            playerDict['outfitter'] = attrs.get_outfitter()
            playerDict['contractExpires'] = attrs.get_contract_expires()
            playerDict['score'] = attrs.get_score()
            playerDict['country'] = attrs.get_country()
            playerDict['price'] = attrs.get_price()
            lstmakedf.append(playerDict)
        self.df = pd.DataFrame.from_records(lstmakedf)
        return self.df
    def save_df(self, pathtosave, filename, extention = 'csv'):
        os.makedirs(pathtosave, exist_ok=True)
        self.df.to_csv('{}/{}.{}'.format(pathtosave, filename, extention), encoding='utf-8')
        return('>>successfully, write df into {}/{}.{}'.format(pathtosave, filename, extention))

def automatic_dowload_raw_data():
    #dowload pageleague
    DowloadPage().dowload(PATH_TO_PROJECT + '/data/support/page_leagues')
    #get urls team
    getUrlTeam = GetUrlTeams()
    print(getUrlTeam.read_url_teams(PATH_TO_PROJECT+'/data/support/page_leagues'))
    print(getUrlTeam.write_url_team(PATH_TO_PROJECT+'/data/support', 'lst_teams'))
    #dowload pageclubs
    with open(PATH_TO_PROJECT + '/data/support/lst_teams.txt', 'r') as fr:
        urls = fr.readlines()
    DowloadPage(urls=urls).dowload(PATH_TO_PROJECT+'/data/support/page_clubs')
    #get url players
    getUrlPlayers = GetUrlPlayers()
    print(getUrlPlayers.read_url_players(PATH_TO_PROJECT+'/data/support/page_clubs'))
    print(getUrlPlayers.write_url_players(PATH_TO_PROJECT+'/data/support', 'lst_players'))
    #dowload page players
    with open(PATH_TO_PROJECT + '/data/support/lst_players.txt', 'r') as fr:
        urls = fr.readlines()
    DowloadPage(urls=urls).dowload(PATH_TO_PROJECT+'/data/support/page_players')
    #Data frame
    getdf = GetDf()
    df = getdf.get_df(PATH_TO_PROJECT + '/data/support/page_players')
    #save df
    df.to_csv(PATH_TO_PROJECT + '/data/raw_data/raw_data.csv', encoding='utf-8', index=False)
    #write date
    with open(PATH_TO_PROJECT+'/data/support/date.txt', 'w', encoding='utf-8') as fw:
        fw.write(str(date.today()))



