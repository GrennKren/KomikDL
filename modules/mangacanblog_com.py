# Kasus di mangacanblog, tidak ada header content-length, jadi harus ngedownload seperti biasa bahkan meskipun hanya untuk memeriksa ukuran gambar saja

from bs4 import BeautifulSoup
import cfscrape
import re
class helper():
    def __init__(self, url):
        self.__kontenHalaman = ''
        self.__url = url

    @property
    def url(self):
        return re.sub('(.+)-\d+(\.html)$', '\g<1>\g<2>', self.__url)
    @url.setter
    def url(self,url):
        self.__url = url
        
    @property
    def title_halaman(self):
        return BeautifulSoup(self.__kontenHalaman,features='html.parser').title.text.lower()
    
    @property    
    def judul(self):
        title = self.title_halaman
        judul = title.split('chapter')[0].title().split("/")[0]
        judul = judul.split(" ", 1)[1].title().strip() #Menghilangkan kata 'Komik' di depan Title
        return judul
    
    @property
    def chapter(self):
        title = self.title_halaman
        chapter = re.sub('.+chapter ([\d\-\_\s\.]+).+','\g<1>',title)
        chapter = re.sub('-','.',chapter)
        if(chapter.find('.') < 0):
            chapter = re.sub('\s+','.',chapter.strip())
        else:
            chapter = re.sub('\s','',chapter.strip())
        return chapter
          
    def CSSSelector(self,choice):
        if(choice == 'all_chapters_url'):
            return "table.updates a"
        elif(choice == 'all_images_url'):
            return "#manga img"
        elif(choice == 'front_page'):
            return '.navbar td a:not(:first-child)'
            
    def parseContent(self,content=''):
        self.__kontenHalaman = content
        
    @property
    def isWholeChapters(self):
        requests = cfscrape.create_scraper()
        req = requests.get(self.url,allow_redirects=True)
        title = BeautifulSoup(req.content,features='html.parser').title.text.lower()
        if(re.search('mangacanblog apk android',title)):
            return True
        else:
            return False       
    