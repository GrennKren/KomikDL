from os import listdir
from os.path import isfile
from os.path import exists
from os import remove
from PIL import Image
from PIL import UnidentifiedImageError
from re import sub
from re import match

_metode = Image.LANCZOS # ada PIL.Image.LANCZOS, PIL.Image.BILINEAR, PIL.Image.NEAREST, dan PIL.Image.BICUBIC. klo argumen 'resample' nya ga disertakan ya gpp. Ntar yg dipilih bilinear (Keknya)
def SimpanPDF(path="",target_lebar=980, judul=''):
    if(not path or not judul):
        return False
    _listFile = [x for x in listdir(path) if isfile(f"{path}\\{x}")]
    try:
        _listFile = list(filter(lambda x:match('.+?\s*-*\s*(\d+)\..+', x),_listFile))
        _listFile.sort(key=lambda x:int(sub('.+?\s*-*\s*(\d+)\..+','\g<1>',x)))
    except:
        print('Terjadi kesalahan saat sorting gambar')
        return False
    _nama_file = path + "\\" + judul + ".pdf"
    remove(_nama_file) if exists(_nama_file) else False
    for _ in _listFile:
        if(_ == _nama_file):
            continue
        try:
            with Image.open(f"{path}\\{_}") as f:
                f_lebar = f.size[0]
                f_tinggi = f.size[1]
                rasio = target_lebar / f_lebar
                if(not exists(_nama_file)):
                    f.convert('RGB').resize((int(f_lebar * rasio), int(f_tinggi * rasio)),resample=_metode).save(_nama_file)
                else:
                    f.convert('RGB').resize((int(f_lebar * rasio), int(f_tinggi * rasio)),resample=_metode).save(_nama_file ,append=True)
        except PermissionError:
            print('Tidak bisa menyimpan ke PDF dikarenakan PDF yang dimaksud sudah terbuka di awal, mohon tutup terlebih dahulu')
            return False
        except UnidentifiedImageError:
            continue
        except Exception as msg:
            print(msg)
            return False
            
    return True