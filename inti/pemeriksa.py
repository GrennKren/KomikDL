from .pengelola import URL
from os import get_terminal_size
from requests.exceptions import ConnectTimeout

class Pemeriksa(URL):
    def periksa_chapter(self, cepat = False, detil_komik = {}):
        
        domain_website = detil_komik['domain_website']
        nomor_chapter  = detil_komik['chapter'] 
        judul_series   = detil_komik['judul']
        
        def cetak_detail(end='\n'):
            nonlocal judul_series
            lbr_terminal = get_terminal_size().columns
            tmp_output = f"{domain_website} - {judul_series} Chapter {nomor_chapter}"
            _jarak_judul = (lbr_terminal - (len(tmp_output) + len(end)) - 1)
            if(_jarak_judul <= 0):
                _judul = judul_series[:_jarak_judul-2]+".."
            else:
                _judul = judul_series
            print(''.ljust(lbr_terminal-1),end='\r')
            output = f"{domain_website} - {_judul} Chapter {nomor_chapter}"
            print(output, end = end+"\r" if end != '\n' else '\n')
            
        cetak_detail(end =' | Memeriksa...')
        
        req = self.requestGet(self.url);
        konten_halaman = req.content
        URLs = self.get_all_images_url(konten_halaman)
        pointer = i_awal,i_tengah,i_kanan = 0,int(len(URLs)/2),len(URLs)-1
        index = 0;
        for i,v in enumerate(URLs):
            if(cepat and i not in pointer):
                continue
            cetak_detail(end =f' | Memeriksa...({i+1}/{len(URLs)})')
            try:
                req = self.requestHead(v)
                if(not req.ok):
                    if(req.status_code == 404):
                        raise Exception
                    else:
                        continue
                        
                content_type = req.headers.get('content-type')
                format_file = self.get_format_file(content_type)
                if(format_file):
                    index+=1
                    
                    content_length = req.headers.get('content-length') or False
                    if(not content_length):
                        req = self.requestGet(v,stream=True)
                        content_length = len(req.content) 
                       
                    if(int(content_length) < 1024):
                        raise Exception
                else:
                    continue
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except ConnectTimeout:
                raise Exception('    Request Timeout')
            except Exception:
                cetak_detail(end =' | [Rusak]\n')
                return
          
        if(cepat):
            cetak_detail(end =' | [Mungkin_Aman]')
        else:
            cetak_detail(end =' | [Aman]')        
        print('')