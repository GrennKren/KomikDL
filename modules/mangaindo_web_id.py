from bs4 import BeautifulSoup
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
    def title_halaman(self):
        return BeautifulSoup(self.__kontenHalaman,features='html.parser').title.text.lower()
    
    @property
    def judul(self):
        title = self.title_halaman 
        judul = title.split('chapter')[0].strip()[:-1].strip().split("/")[0].title().strip()
        return judul
    
    @property
    def chapter(self):
        title = self.title_halaman 
        chapter = re.sub('.+chapter ([\d\-\_\s\.]+).+','\g<1>',title)
        chapter = re.sub('-','.',chapter)
        
        if(chapter.find('.') < 0):
            chapter = re.sub('\s+','-',chapter.strip())
        else:
            chapter = re.sub('\s','',chapter.strip())
        return chapter
    
    def CSSSelector(self,choice):
        if(choice == 'all_chapters_url'):
            return ".lcp_catlist a"
        elif(choice == 'all_images_url'):
            return '.entry-content img'
        elif(choice == 'front_page'):
            return {'url':re.sub('(.+?)(\-indonesia)?-chapter.+\/?', '\g<1>', self.__url)}
        
    def parseContent(self,content=''):
        self.__kontenHalaman = content
    
    @property
    def isWholeChapters(self):
        if(re.match('.+chapter?.+?([\d\-]*)/?',self.__url)):
            return False
        else:
            return True       
        