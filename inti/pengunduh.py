from .pengelola import URL
from os.path import exists
from os import mkdir
from re import sub
from .pdf import SimpanPDF 
from requests.exceptions import ConnectTimeout

class Pengunduh(URL):
    def unduh(self,cetak_pdf = False, detil_komik = {}):
        
        domain_website = detil_komik['domain_website']
        nomor_chapter  = detil_komik['chapter'] 
        judul_series   = detil_komik['judul']
        lokasi_website = detil_komik['lokasi_website']
        lokasi_judul   = detil_komik['lokasi_judul']
        lokasi_output  = detil_komik['lokasi_output']
        
        print(f"{domain_website} - {judul_series} Chapter {nomor_chapter}")
        
        req = self.requestGet(self.url);
        konten_halaman = req.content
        URLs = self.get_all_images_url(konten_halaman)
        index = 0;
        for i,v in enumerate(URLs):
            try:
                
                req = self.requestHead(v)
                if(not req.ok):
                    if(req.status_code == 404):
                        raise Exception('Gambar tidak ditemukan dengan kode respon ' + req.status_code)
                    else:
                        continue
                        
                format_file = self.get_format_file(req.headers.get('content-type'))
                if(format_file):
                    index+=1
                    
                    output_gambar = f"{lokasi_output}\\Chapter {nomor_chapter} - {index}.{format_file}"
                    content_length = req.headers.get('content-length') or False
                    
                    if(not content_length):
                        req = self.requestGet(v,stream=True)
                        content_length = len(req.content) 
                    
                    if(exists(output_gambar)):
                        with open(output_gambar,'r') as f:
                            fsize = f.seek(0,2)
                        if(int(content_length) == fsize):
                            raise Exception('Sudah ada')
                    if(int(content_length) < 1024):
                        raise Exception('Ukuran terlalu kecil ataupun sudah rusak')
                    if(not req.content):
                        req = self.requestGet(v,stream=True)
                    
                    
                    if not exists(lokasi_website):
                        mkdir(lokasi_website)
                    if not exists(lokasi_judul):
                        mkdir(lokasi_judul)
                    if not exists(lokasi_output):
                        mkdir(lokasi_output)   
                    
                    with open(output_gambar,'wb') as f:
                        f.write(req.content)
                    
                    print(str(i+1) + ") Chapter " + nomor_chapter + " - " +  str(index) + "." + format_file)
                            
                else:
                    raise Exception('format gambar tidak sesuai')
            except ConnectTimeout:
                raise Exception('    Request Timeout')
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as msg:
                print("{}) Skipped - alasan : {}".format(str(i+1),msg) )
                continue
                
        print("")
        
        if(cetak_pdf):
            _nama_pdf = f"{domain_website} - {judul_series} Chapter {nomor_chapter}"
            result_pdf = SimpanPDF(path=lokasi_output,target_lebar=self.lebar_pdf, nama_pdf =sub('[\\\/\:\*\?\"\<\>\|]','',_nama_pdf))
            if(result_pdf):
                print('Berhasil menyimpan ke PDF\n')
            else:
                print('Terjadi kesalahan saat menyimpan ke PDF\n')
            
        return   