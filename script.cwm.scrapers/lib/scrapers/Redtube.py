import requests
from bs4 import BeautifulSoup
import xbmcgui
import re
dialog = xbmcgui.Dialog()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
Base_Domain = 'https://www.redtube.com'
class Scraper:
    def __init__(self):
        self.Base = 'https://www.redtube.com/?page=1'
        self.CatUrl = 'https://www.redtube.com/categories'
        self.Search = ('https://www.redtube.com/?search=%s')
        self.content = []
        self.links = []
        self.cats = []
    def SearchSite(self,term):
        term = term.replace(' ','+')
        link = requests.get(self.Search%term,headers=headers).text
        soup = BeautifulSoup(link,'html.parser')
        data = soup.find_all('span', class_={'video_thumb_wrap'})
        for i in data:
            try:
                title = i.img['alt']
                icon = i.img['data-src']
                media = i.a['href']
                if not Base_Domain in media: media = Base_Domain+media
                self.content.append({'name' : title, 'url': media, 'image' : icon})
            except: pass
        return self.content
    def MainContent(self,url):
        if url == '': url = self.Base
        link = requests.get(url,headers=headers).text
        soup = BeautifulSoup(link,'html.parser')
        data = soup.find_all('span', class_={'video_thumb_wrap'})
        for i in data:
            try:
                title = i.img['alt']
                icon = i.img['data-src']
                media = i.a['href']
                if not Base_Domain in media: media = Base_Domain+media
                self.content.append({'name' : title, 'url': media, 'image' : icon})
            except: pass
        return self.content
    def ResolveLink(self,url):
        link = requests.get(url, headers=headers).text
        pattern = r'''videoUrl['"]:['"]([^"]+)['"]'''
        source = re.findall(pattern,link,flags=re.DOTALL)[0].replace('\\','')
        source = 'https://www.redtube.com'+source
        link = requests.get(source,headers=headers).json()
        for i in link:
            qual = i['quality']
            url = i['videoUrl']
            self.links.append({'name' : str(qual), 'url': url})
        return self.links
    def GetCats(self):
        c = requests.get(self.CatUrl,headers=headers).text
        soup = BeautifulSoup(c,'html.parser')
        r = soup.find('ul', id={'categories_list_block'})
        for i in r.find_all('a', class_={'category_thumb_link'}):
            try:
                title = i.img['alt']
                url = i['href']
                if not Base_Domain in url: url = Base_Domain+url
                self.cats.append({'name' : title, 'url': url+'?page=1'})
            except: pass
        return self.cats
    def GetNextPage(self,url):
        if url == '':
            url = 'https://www.redtube.com/?page=2'
            return url
        else:
            if not '/redtube/' in url:
                getcurrent = re.findall(r'\d+',url)[0]
                NewNextPageUrl = int(getcurrent) + 1
                NextPageUrl = ('https://www.redtube.com/?page=%s' % NewNextPageUrl)
                return NextPageUrl
            else:
                oldurl = url.rsplit('page=', 1)[0]
                getcurrent = re.findall(r'\d+',url)[0]
                NewNextPageUrl = int(getcurrent) + 1
                NextPageUrl = ('%spage=%s' % (oldurl,NewNextPageUrl))
                return NextPageUrl