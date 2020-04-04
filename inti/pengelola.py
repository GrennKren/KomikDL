from importlib import import_module
from urllib.parse import urlparse
from re import sub
from re import search
from os.path import exists
from os import mkdir
from os import get_terminal_size
from cfscrape import create_scraper
from tldextract import TLDExtract
from tldextract import extract
from bs4 import BeautifulSoup

from requests.exceptions import SSLError
from requests.exceptions import MissingSchema
from requests.exceptions import ConnectTimeout

from . import konfigurasi as konfig

HEADERS       = {'Accept' : 'image/jpg'}
TIMEOUT       = konfig.timeout
DEFAULT_PATH  = konfig.default_path
browser       = create_scraper()
domainExtract = TLDExtract(cache_file=DEFAULT_PATH+"\\cache_domain_TLD.txt")
LEBAR_PDF     = konfig.lebar_pdf
    
##=======================================================================##
class URL():
    def __init__(self,url):
        self.website = domainExtract(url).registered_domain
        try:
            url = self.normalisasi_url(url)
            self.__url = url
            self.website = domainExtract(url).registered_domain
            self.lebar_pdf = LEBAR_PDF
        except Exception as msg:
            raise Exception(msg)
            return      
        self.modul = self.nama_modul
        
    @property
    def website(self):
        return self.__website
    @website.setter
    def website(self,url):
        self.__website = domainExtract(url).registered_domain
    
    @property
    def nama_modul(self):
        return self.website.replace('.','_').lower()
    
    @property
    def modul(self):
        return self.__modul
    @modul.setter
    def modul(self,m):
        try:
            modul = import_module('modules.' + m)
            self.__modul = modul.helper(self.url)
            self.url = self.modul.url
        except:
            raise Exception('Tidak ditemukan modul yang sesuai dengan ' + m)
            return
        return True
    
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self,url):
        self.__url = url
        
    def get_all_images_url(self, c = ""):
        listImages = BeautifulSoup(c ,features='html.parser').select(self.modul.CSSSelector('all_images_url'))
        listURL = []
        for i in listImages:
            url = BeautifulSoup(str(i),features='html.parser').find('img')['src']
            url = sub('\\t|\\n','',url)
            if(urlparse(url).netloc):
                listURL.append(url)
            
        return listURL

    def get_all_chapters_url(self,filter=[],aksi_ambil_total_chapter=False):
        url = self.url
        c = self.requestGet(url).content
        if(aksi_ambil_total_chapter):
            self.modul.url = url
            if(not self.modul.isWholeChapters):
                #tmp = self.requestGet(url)
                if(type(self.modul.CSSSelector('front_page')) == type({})):
                    url = self.modul.CSSSelector('front_page').get('url')
                else:
                    url = BeautifulSoup(c, features='html.parser').select(self.modul.CSSSelector('front_page'))[0]['href']
                c = self.requestGet(url).content
        
        listHyperlink = BeautifulSoup(c, features='html.parser').select(self.modul.CSSSelector('all_chapters_url'))
        listURL = []
        for index,i in enumerate(listHyperlink):
            if(filter):
                
                re_1 = '.*chapter ([\d\.]+\s*[\_\-\.]?\s*[\d\.]*).*'
                re_2 = '.*?([\d\.]+)\s*\:.*'
                re_3 = '.+?chapter-(\d+-?\d*).+'
                
                if(search(re_1,i.text.lower())):
                    x = sub(re_1, '\g<1>', i.text.lower())
                elif(search(re_2,i.text.lower())):
                    x = sub(re_2, '\g<1>', i.text.lower())
                elif(search(re_3, str(i))):
                    x = sub(re_3, '\g<1>', str(i).lower())
                else:
                    raise Exception('Tidak menemukan regex yang tepat untuk mencari nomor chapter')
                    return
                
                x = x.replace(' ','').replace('_','.').replace('-','.')
                x = float(sub('\.+','.',x))
                
                if(int(x) in filter):
                    listURL.append(BeautifulSoup(str(i),features='html.parser').find('a')['href'])
                else:
                    # Untuk parameter --chapter yg pake format x-  ('-'/dash di belakang angka)
                    if filter[0] == -1:
                        if x >= filter[-1]: 
                            listURL.append(BeautifulSoup(str(i),features='html.parser').find('a')['href'])
            else:
                listURL.append(BeautifulSoup(str(i),features='html.parser').find('a')['href'])
             
        listURL.reverse()
         
        return listURL
         
    def get_format_file(self, content_type):
        if('jpg' in content_type.lower() or 'jpeg' in content_type.lower()):
            return 'jpg'
        elif('png' in content_type.lower()):
            return 'png'
        else:
            return False

    def decorator_request(requestFunc):
        def complete_request(*input, **input2):
            try:
                req = requestFunc(*input, **input2)
            except SSLError:
                url = input[-1]
                req = requestFunc(url, **input2)
            class extend_requests():
                def __init__(self):
                    title = ''
                    if('html' in req.headers.get('content-type').lower()):
                        if(req.content):
                            title = BeautifulSoup(req.content,features='html.parser').title.text.split('-')[0].strip()
                    for i,v in req.__dict__.items():
                        self.__dict__[i] = v
                        
                    self.__dict__['title'] = title
                    self.__dict__['ok'] = req.status_code == 200 or False
                    self.__dict__['content'] = req.content
            result = extend_requests()
            return result
        return complete_request
        
    @decorator_request
    def requestGet(self,url,allow_redirects = True, stream = False, headers = HEADERS, timeout = TIMEOUT):
        req = browser.get(url, allow_redirects=allow_redirects, stream=stream, headers=headers, timeout = timeout)
        return req
    @decorator_request    
    def requestHead(self, url, allow_redirects = True, stream = False, headers = HEADERS, timeout = TIMEOUT):
        req = browser.head(url, allow_redirects = allow_redirects, stream=stream, headers=headers, timeout = timeout)
        return req
    
    def normalisasi_url(self,url):
        website = domainExtract(url).registered_domain.capitalize()
        coba_url = url
        coba_url = f'{website}/{url}' if not domainExtract(url).suffix else coba_url
        coba_url = f'https://{website}/{url}' if not urlparse(url).scheme else coba_url
        return coba_url
    
    def start_proses(self, url="",aksi_periksa=False, aksi_periksa_cepat=False, aksi_ambil_total_chapter = False, simpan_pdf = False):
        
        if(len(url) < 1):
            url = self.url
        try:
            
            request = self.requestHead(url)
            url = request.url
            if(request.ok):
                request_halaman = self.requestGet(url)
                if(request_halaman.ok):
                    konten_halaman = request_halaman.content
                    
                    #####################################
                    modul = self.modul
                    modul.parseContent(konten_halaman)
                    judul = modul.judul.strip()
                    chapter = modul.chapter
                    
                    domain_website = domainExtract(url).registered_domain.capitalize()
                    
                    folder_website = DEFAULT_PATH + "\\" + domain_website
                    folder_judul = folder_website + "\\" + sub('[\\\/\:\*\?\"\<\>\|]','',judul)
                    folder_keluaran = folder_judul + "\Chapter " + chapter 
                    ######################################
                    _detil_komik = {
                        'judul':judul,
                        'chapter':chapter,
                        'domain_website':domain_website,
                        'lokasi_website':folder_website,
                        'lokasi_judul':folder_judul,
                        'lokasi_output':folder_keluaran
                    }
                    #################
                    
                    if(aksi_periksa or aksi_periksa_cepat):
                        from .pemeriksa import Pemeriksa
                        p = Pemeriksa(url)
                        p.periksa_chapter(aksi_periksa_cepat, _detil_komik)
                        return                 
                    #################
                    if(aksi_ambil_total_chapter):
                        modul.url = url
                        daftar_chapter = self.get_all_chapters_url(aksi_ambil_total_chapter=True)
                        print("{} - {} | Total Chapter : {}".format(domain_website, judul, len(daftar_chapter)))
                        return
                    #################
                    
                    from .pengunduh import Pengunduh
                    p = Pengunduh(url)
                    p.unduh(simpan_pdf,_detil_komik)
                    return          
        except Exception as msg:
            raise Exception(msg)
            return False    

def tindakan(url, **parameter):
    try:
        d = URL(url)
        d.modul = d.nama_modul
        url = d.modul.url
        
        daftar_index = parameter['daftar_index']
        get_total_chapter = parameter['get_total_chapter']
        aksi_periksa = parameter['aksi_periksa']
        aksi_periksa_cepat=parameter['aksi_periksa_cepat']
        simpan_pdf = parameter['simpan_pdf']
        
        if(d.modul.isWholeChapters):
            terbaru = parameter['terbaru']
            URLs = d.get_all_chapters_url(filter=daftar_index)   
            
            if(terbaru):
                URLs.reverse()
            for i in URLs:
                d.start_proses(i, aksi_periksa, aksi_periksa_cepat, get_total_chapter, simpan_pdf)
                if(get_total_chapter):
                    return
        else:  
            d.start_proses(url, aksi_periksa, aksi_periksa_cepat, get_total_chapter, simpan_pdf) 
        
    except KeyboardInterrupt:
        print('\nPengguna telah mengakhiri program')
        return
    except Exception as msg:
        print(msg)
        return 
        
