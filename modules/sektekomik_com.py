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
        judul = judul.split('chapter')[0].split("/")[0].title().strip()
        return judul
    
    @property
    def chapter(self):
        chapter = BeautifulSoup(self.__kontenHalaman,features='html.parser').title.text.lower()
        chapter = re.sub('.+chapter ([\d\-\_\s\.]+).+','\g<1>',chapter)
        chapter = re.sub('-','.',chapter)
        if(chapter.find('.') < 0):
            chapter = re.sub('\s+','.',chapter.strip())
        else:
            chapter = re.sub('\s','',chapter.strip())
        return chapter
    
    def CSSSelector(self,choice):
        if(choice == 'all_chapters_url'):
            return ".lchx a"
        elif(choice == 'all_images_url'):
            return '#readerarea img'
        elif(choice == 'front_page'):
            return '.headpost .allc a'
            
    def parseContent(self,content=''):
        self.__kontenHalaman = content
    
    @property
    def isWholeChapters(self):
        sectionURL = list(filter(None,self.__url.split('/')))
        
        if(sectionURL[2] == 'manga'):
            return True
        else:
            return False       
        