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

from .pdf import SimpanPDF 
from . import konfigurasi as konfig

HEADERS       = {'Accept' : 'image/jpg'}
LEBAR_PDF     = konfig.lebar_pdf
TIMEOUT       = konfig.timeout
DEFAULT_PATH  = konfig.default_path
browser       = create_scraper()
domainExtract = TLDExtract(cache_file=DEFAULT_PATH+"\\tldextract.txt")

class URL():
    
    def __init__(self,url):
        self.website = domainExtract(url).registered_domain
        try:
            url = self.normalisasi_url(url)
            self.__url = url
            self.website = domainExtract(url).registered_domain
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
        return self.website.replace('.','_')
    
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
            if(urlparse(url).netloc):
                listURL.append(url)
            
        return listURL

    def get_all_chapters_url(self,filter=[],aksi_ambil_total_chapter=False):
        url = self.url
        c = self.requestGet(url).content
        if(aksi_ambil_total_chapter):
            self.modul.url = url
            if(not self.modul.isWholeChapters):
                tmp = self.requestGet(self.url)
                url = BeautifulSoup(c, features='html.parser').select(self.modul.CSSSelector('front_page'))[0]['href']
                c = self.requestGet(url).content
        
        listHyperlink = BeautifulSoup(c, features='html.parser').select(self.modul.CSSSelector('all_chapters_url'))
        listURL = []
        for index,i in enumerate(listHyperlink):
            if(filter):
                re_1 = '.*chapter ([\d\.]+\s*[\_\-\.]?\s*[\d\.]*).*'
                re_2 = '.*?([\d\.]+)\s*\:.*'
                if(search(re_1,i.text.lower())):
                    x = sub(re_1,'\g<1>',i.text.lower())
                elif(search(re_2,i.text.lower())):
                    x = sub(re_2, '\g<1>', i.text.lower())
                else:
                    raise Exception('Tidak menemukan regex yang tepat untuk mencari nomor chapter')
                    return
                x = x.replace(' ','').replace('_','.').replace('-','.')
                x = float(sub('\.+','.',x))
                
                if(int(x) in filter):
                    listURL.append(BeautifulSoup(str(i),features='html.parser').find('a')['href'])
                else:
                    # Untuk parameter --range yg pake format x-  ('-'/dash di belakang angka)
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
            req = requestFunc(*input, **input2)
           
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
        website = self.website
        coba_url = url
        while(True):
            try: 
                r = self.requestHead(coba_url)
                if(r.ok):
                    return r.url
                elif(r.status_code == 404):
                    raise Exception(f'Dengan status response code 404 alias tidak ditemukan nya URL\n"{coba_url}"')
            except MissingSchema:
                coba_url = f'https://{website}/{url}' if not domainExtract(url).suffix else f'https://{url}'
            except UnicodeError:
                coba_url = f'https://{website}/{url}' if not domainExtract(url).suffix else f'https://{url}'
            except SSLError:
                coba_url = 'http://' + url
            except Exception as msg:
                raise Exception("Tidak dapat terhubung dengan : " + website + "\n" + str(msg))
                return
            
    def start_proses(self,url="", aksi_periksa=False, daftar_index=[], aksi_ambil_total_chapter = False, simpan_pdf = False):
        
        if(len(url) < 1):
            url = self.url
        try:
            
            request = self.requestHead(url)
            if(request.ok):
                request_halaman = self.requestGet(url)
                if(request_halaman.ok):
                    konten_halaman = request_halaman.content
                    
                    #####################################
                    modul = self.modul
                    modul.parseContent(konten_halaman)
                    judul = modul.judul.strip()
                    chapter = modul.chapter
                    
                    domain_website = self.website.capitalize()
                    
                    folder_website = DEFAULT_PATH + "\\" + domain_website
                    folder_judul = folder_website + "\\" + judul
                    folder_keluaran = folder_judul + "\Chapter " + chapter 
                    ######################################
                    
                    if(aksi_ambil_total_chapter):
                        daftar_chapter = self.get_all_chapters_url(aksi_ambil_total_chapter=True)
                        print("{} - {} | Total Chapter : {}".format(domain_website, judul, len(daftar_chapter)))
                        return
                    
                    def cetak_detail_judul(end='\n', end_2 = ''):
                        nonlocal judul
                        pondasi = "{} - {} Chapter {}"
                        lbr_terminal = get_terminal_size().columns
                        temp_string = pondasi.format(domain_website,judul,chapter)
                        
                        _jarak_judul = (lbr_terminal - (len(temp_string) + len(end)) - 1)
                        if(_jarak_judul < 0):
                            _judul = judul[:_jarak_judul-2]+".."
                        else:
                            _judul = judul
                        string = pondasi.format(domain_website,_judul,chapter)
                        
                        print(''.ljust(lbr_terminal-1),end='\r')
                        print(string, end = end+"\r"+end_2 if end != '\n' else '\n')
                    
                    cetak_detail_judul(end ='\n' if not aksi_periksa else ' | Memeriksa...')
                    
                    URLs = self.get_all_images_url(konten_halaman)
                    index = 0;
                    
                    for i,v in enumerate(URLs): #URL GAMBARNYA
                        if(aksi_periksa):
                            cetak_detail_judul(end =' | Memeriksa...({}/{})'.format(i+1,len(URLs)))
                        try:
                            req = self.requestHead(v)
                            if(not req.ok):
                                raise Exception('Gambar tidak ditemukan dengan kode respon ' + req.status_code)
                            
                            format_file = self.get_format_file(req.headers.get('content-type'))
                            if(format_file):
                                index+=1
                                
                                file_download = "{}\\Chapter {} - {}.{}".format(folder_keluaran, chapter, index, format_file)
                                content_length = req.headers.get('content-length') or False
                                
                                if(not content_length):
                                    req = self.requestGet(v,stream=True,timeout=TIMEOUT*1.5)
                                    content_length = len(req.content) 
                                if(not aksi_periksa):
                                    if(exists(file_download)):
                                        with open(file_download,'r') as f:
                                            fsize = f.seek(0,2)
                                        if(int(content_length) == fsize):
                                            raise Exception('Sudah ada')
                                
                                    if(not req.content):
                                        req = self.requestGet(v,stream=True,timeout=TIMEOUT*1.5)
                                    
                                if(int(content_length) < 1024):
                                    raise Exception('Ukuran terlalu kecil ataupun sudah rusak')
                                
                                if(not aksi_periksa):
                                    if not exists(folder_website):
                                        mkdir(folder_website)
                                    if not exists(folder_judul):
                                        mkdir(folder_judul)
                                    if not exists(folder_keluaran):
                                        mkdir(folder_keluaran)   
                                    
                                    with open(file_download,'wb') as f:
                                        f.write(req.content)
                                    
                                    print(str(i+1) + ") Chapter " + chapter + " - " +  str(index) + "." + format_file)
                                        
                            else:
                                if(aksi_periksa): #Kupikir hanya karena format gambar nya ga sesuai bukan berarti rusak
                                    continue
                                raise Exception('format gambar tidak sesuai')
                        except ConnectTimeout:
                            raise Exception('    Request Timeout')
                        except Exception as msg:
                            if(not aksi_periksa):
                                print("{}) Skipped - alasan : {}".format(str(i+1),msg) )
                                continue
                            else:
                                cetak_detail_judul(end =' | [Rusak]',end_2='\n')
                                return
                                
                    cetak_detail_judul(end =' | [Aman]',end_2='\n') if aksi_periksa else False
                    print("") if not aksi_periksa else False
                    if(simpan_pdf):
                        _judul = f"{domain_website} - {judul} Chapter {chapter}"
                        result_pdf = SimpanPDF(path=folder_keluaran,target_lebar=LEBAR_PDF,judul=_judul)
                        if(result_pdf):
                            print('Berhasil menyimpan ke PDF\n')
                        else:
                            print('Terjadi kesalahan saat menyimpan ke PDF\n')
                        
                    return          
        except Exception as msg:
            raise Exception("Tidak dapat terhubung dengan : " + self.website + "\n" + str(msg))
            return False    

def tindakan(url, **parameter):
    try:
        d = URL(url) # url nya Dalam bentuk string
        daftar_index = parameter['daftar_index'] # Dalam bentuk list
        get_total_chapter = parameter['get_total_chapter'] # True or False
        aksi_periksa = parameter['aksi_periksa'] # True or False
        simpan_pdf = parameter['simpan_pdf'] # True or False
        if(d.modul.isWholeChapters):
            terbaru = parameter['terbaru']
            URLs = d.get_all_chapters_url(filter=daftar_index)   
            
            if(terbaru):
                URLs.reverse()
            for i in URLs:
                i = d.normalisasi_url(i)
                d.modul.url = i
                d.start_proses(d.modul.url, aksi_periksa=aksi_periksa, aksi_ambil_total_chapter = get_total_chapter, simpan_pdf=simpan_pdf)
                if(get_total_chapter):
                    return
        else:   
            # parameter daftar_index ku ilangin disini, bila dipakai itu kumpulan indeks digunakan untuk hanya untuk mendownload page nya bedasarkan nomornya. Tak berguna kah?
            d.start_proses(aksi_periksa=parameter['aksi_periksa'], aksi_ambil_total_chapter = get_total_chapter, simpan_pdf = simpan_pdf) 
        
    except KeyboardInterrupt:
        print('\nPengguna telah mengakhiri program')
        return
    except Exception as msg:
        print(msg)
        return 
        
