from os.path import expanduser
from configparser import ConfigParser

home = expanduser('~')
lokasi_konfig = home + "\\komikdl.conf"

konfig = ConfigParser()
konfig.read(lokasi_konfig)

if(len(konfig.items()) <= 1):
    konfig.add_section('penyimpanan')
    konfig.add_section('argumen_url')
    konfig.add_section('pdf')
    konfig.set('penyimpanan', 'nama_folder' , 'KomikDL')
    konfig.set('penyimpanan', 'default_path', '')
    konfig.set('argumen_url', 'timeout', '20')
    konfig.set('pdf', 'lebar_pdf', '800')
    
    with open(lokasi_konfig, 'w') as f:
        konfig.write(f)

nama_folder = konfig.get('penyimpanan', 'nama_folder' ).strip('"').strip().strip("'")
default_path = konfig.get('penyimpanan', 'default_path').strip('"').strip().strip("'")
timeout = konfig.getint('argumen_url', 'timeout')
lebar_pdf = konfig.getint('pdf', 'lebar_pdf')

if len(default_path) < 1:
    default_path = "{}\\{}".format(home,nama_folder)
else:
    default_path = "{}\\{}".format(default_path,nama_folder)

