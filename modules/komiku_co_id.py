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
        judul = re.sub('(.+?)\s[chapter]{6,7}.+','\g<1>', title).split("/")[0]
        judul = judul.split(" ", 1)[1].title().strip() #Menghilangkan kata 'Komik' di depan Title
        return judul
    
    @property
    def chapter(self):
        title = self.title_halaman 
        chapter = re.sub('.+?\s[chapter]{6,7} ([\d\-\_\s\.]+).+','\g<1>',title)
        chapter = re.sub('-','.',chapter)
        
        if(chapter.find('.') < 0):
            chapter = re.sub('\s+','.',chapter.strip())
        else:
            chapter = re.sub('\s','',chapter.strip())
        return chapter.strip('.')
    
    def CSSSelector(self,choice):
        if(choice == 'all_chapters_url'):
            return "#Chapter .judulseries a"
        elif(choice == 'all_images_url'):
            return "#Baca_Komik img"
        elif(choice == 'front_page'):
            return ".tbl td b a"
    def parseContent(self,content=''):
        self.__kontenHalaman = content
    
    @property
    def isWholeChapters(self):
        sectionURL = list(filter(None,self.__url.split('/')))
        if(sectionURL[2] == 'manga'):
            return True
        else:
            return False       
        