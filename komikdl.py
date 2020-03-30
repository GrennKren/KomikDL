from os import mkdir
from os.path import exists
from argparse import ArgumentParser

import inti.konfigurasi as konfig
from inti import tindakan
from re import sub
from re import search
from sys import argv

def _aksi(URL='',**parameter):
    DEFAULT_PATH = konfig.default_path
    
    if(exists(DEFAULT_PATH) == False):
        mkdir(DEFAULT_PATH)
    
    if(len(URL.strip()) > 0):
        tindakan(URL, **parameter)
    else:
        print('alamat URL belum dimasukkan')
        

def get_index(daftar_index=[]):
    
    if(daftar_index):
        daftar_index = list(filter(None,daftar_index.split(',')))
        daftar_index = [x.replace(" ","") for x in daftar_index if bool(search('[^\d\s\.-]',x)) == False] #menyaring karakter yang bukan '-' dan angka
        daftar_index.sort()
    result_range = []
    for i,v in enumerate(daftar_index): 
        if(search('^-',v)):
            v = int(sub('^-([\d\.]+)','\g<1>',v))
            [result_range.append(x) for x in range(0,v+1)]
        elif(search('-$',v)):
            v = float(sub('([\d\.]+)-$','\g<1>',v))
            result_range.append(float(v))
            result_range.append(-1)
        elif(search('([\d\.]+)-([\d\.]+)',v)):
            v = sub('([\d\.]+)-([\d\.]+)','\g<1>,\g<2>',v).split(',')
            v = list(map(int,v))
            v.sort()
            [result_range.append(x) for x in range(v[0],v[1]+1)]
        else:
            result_range.append(float(v))
    result_range = list(set(result_range)) #!kurang paham ama hasil urutan function nya SET , tes aja ... set([5,6,7,8]) hasil nya malah 8,5,6,7
    result_range.sort()
    return result_range
    
def get_lines(_input_file=''):
    try:
        with open(_input_file,'r') as f:
            i = f.read().splitlines()
        return list(filter(None,i))    
    except FileNotFoundError:
        return False
#================================================================
# Urutan prioritas argumen (ga perlu disesuaikan urutan argumen pas eksekusi programnya)
# 1) url (harus ada)
# 2) --input-file LOKASI_FILE (Jika ini disertakan, parameter 3,4,dan 5 di hiraukan. Tapi parameter2 tersebut bisa diletakan disamping tiap baris dari url di file) 
# 3) -get-total-chapter
# 3) --periksa / --check (Tidak mendownload gambar, hanya memeriksa jika salah satu gambar ada yang rusak di chapter)
# 4) --chapter -4,5,6,7-9,10- (Menentukan no chapter atau gambar yang mau di download atau di cek. x-x untuk dari nomor sekian ke sekian, "-x" untuk dari awal sampai nomor x, "x-" untuk dari nomor x ke akhir
# 5) --terbaru (Mendownload ataupun hanya sekedar memeriksa (parameter --periksa) dari chapter terbaru)
#
#
#

def main():
    input = ArgumentParser()
    input.add_argument('url', nargs='*')
    input.add_argument('--input-file')
    input.add_argument('--chapter',dest='range',type=list,default=[])
    input.add_argument('--terbaru', dest='terbaru',action='store_true')
    input.add_argument('--reverse', dest='terbaru',action='store_true')
    input.add_argument('--periksa', dest='cek', action='store_true')
    input.add_argument('--periksa-cepat', dest='cek_cepat', action='store_true')
    input.add_argument('--total-chapter', action='store_true')
    input.add_argument('--pdf', action='store_true')
    
    def split_argument(a): 
        #a = " ".join(a).split()
        for i,v in enumerate(a):
            if a[i-1] == '--chapter':
                a.__setitem__(i,v.split())
        return a #sengaja menghandle sendiri parsing argument, agar tanda koma (,) ama dash (-) bisa digunakan secara leluasa di parameter --range
                
    def handle_argument(i):
        
        nonlocal tmp_path_file,input
        if(i):
            for _ in i: 
                _input = input.parse_args(split_argument(_.split()))
                 
                input_file = _input.input_file
                if(input_file):
                    if(input_file not in tmp_path_file):
                        tmp_path_file.append(input_file)
                        _list_baris = get_lines(input_file)
                        if(not _list_baris):
                            continue
                        handle_argument(_list_baris)
                    else:
                        print("Boi.. mau paradox ya. input-file sama persis namanya di dalam input-file")
                        continue
                
                url = _input.url or False
                if(not url):
                    continue
                url = url[0]
                
                daftar_index = get_index("".join(_input.range) if _input.range else [])
                terbaru = _input.terbaru
                cek_cepat = _input.cek_cepat
                cek = True if cek_cepat else _input.cek 
                get_total_chapter = _input.total_chapter
                simpan_pdf = _input.pdf
                
                _aksi(url,daftar_index=daftar_index, aksi_periksa=cek, aksi_periksa_cepat=cek_cepat, terbaru=terbaru, get_total_chapter = get_total_chapter, simpan_pdf=simpan_pdf)    
    
    i = [" ".join(argv[1:])]
    tmp_path_file = []
    handle_argument(i)

if __name__ == '__main__':  
    main()