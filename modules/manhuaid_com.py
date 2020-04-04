from bs4 import BeautifulSoup
import requests
import re

class helper():
    def __init__(self,url):
        self.__kontenHalaman = ''
        self.__url = url
    
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self,url):
        self.__url = url
        
    @property
    def judul(self):
        judul = BeautifulSoup(self.__kontenHalaman,features='html.parser').title.text.lower()
        judul = re.sub('(.+?)\s[chapter]{6,7}.+','\g<1>', judul).split("/")[0].title().strip()
        return judul

    @property
    def chapter(self):
        chapter = BeautifulSoup(self.__kontenHalaman,features='html.parser').title.text.lower()
        chapter = re.sub('.+?\s[chapter]{6,7} ([\d\-\_\s\.]+).+','\g<1>',chapter)
        chapter = re.sub('-','.',chapter)
        if(chapter.find('.') < 0):
            chapter = re.sub('\s+','.',chapter.strip())
        else:
            chapter = re.sub('\s','',chapter.strip())
        return chapter.strip('.')
    
    def CSSSelector(self,choice):
        if(choice == 'all_chapters_url'):
            return ".table td:first-child a"
        elif(choice == 'all_images_url'):
            return ".row .col-md-12 img"
        elif(choice == 'front_page'):
            return '.container a.text-white'
    def parseContent(self,content=''):
        self.__kontenHalaman = content
    
    @property
    def isWholeChapters(self):
        sectionURL = list(filter(None,self.__url.split('/')))
        if(len(sectionURL)<5):
            return True
        else:
            return False       
        