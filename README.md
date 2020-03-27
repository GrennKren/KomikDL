# KomikDL
Program tool berbasis command line / CLI untuk mendownload komik secara otomatis yang dikhususkan hanya situs web komik di Indonesia. 

### Fitur yang ada untuk sekarang
  * Mendownload chapter suatu komik dengan input url yang dimaksud 
  * Mendownload **keseluruhan** chapter
  * Menyimpan hasil download ke dalam bentuk PDF
  * Mencetak total chapter judul yang ada di situs web komik tersebut
  * Melakukan proses memeriksa gambar rusak secara otomatis
  * Mendownload banyak input URL yang diambil di dalam file sebagai input

Untuk mengenai program nya sendiri, ini dibangun menggunakan bahasa pemrograman Python 3 
serta menggunakan beberapa modul yang bukan built-in dari python seperti 
`cfscrape, requests, tldextract, PIL, BeautifulSoup`

Selain dalam bentuk python, program ini juga disediakan stand-alone program nya alias berdiri sendiri 
untuk sistem operasi Windows alias tanpa perlu menginstall sesuatu seperti Python ataupun modul yg saya 
sebutkan di atas. Berterima kasih kepada program `PyInstaller` untuk yg satu ini.

### Contoh Penggunaan
```
  komikdl https://example.com/judul-komik-chapter-525/         (Mendownload chapter 525 nya saja)
  komikdl https://example.com/manga/judul-komik/               (Mendownload kesemua chapter dimulai dari yang terlama)
```

Selain penggunaan di atas ada juga beberapa parameter yang disediakan.
### Parameter
```
  --input-file LokasiFILE , menyertakan lokasi file yang ada di komputer berisikan kumpulan URL yang dipisahkan dengan garis baru / enter.
  --chapter nomor_chapter , memasukkan nomor maupun jangkauan nomor chapter nya agar yang di download hanya nomor2 tersebut.
  --terbaru , Mendownload dimulai dari chapter terbaru. dikarenakan secara default mendownload keseluruhan chapter dimulai dari yang terlama 
  --periksa , Hanya melakukan pemeriksaan cepat untuk menentukan gambar rusak.
  --total-chapter, Mencetak total chapter komik yang ada di situs web di url input
  --pdf , Menyimpan hasil download ke dalam bentuk PDF
```

### Contoh Penggunaan Lengkap
```
  komikdl --chapter 4 https://example.com/manga/judul-komik/                  | untuk mendownload chapter  4 nya saja
  komikdl --chapter 4,7 https://example.com/manga/judul-komik/                | untuk mendownload chapter 4 dan 7
  komikdl --chapter -6 https://example.com/manga/judul-komik/                 | untuk mendownload dari chapter awal ke 6
  komikdl --chapter 9- https://example.com/manga/judul-komik/                 | untuk mendownload dari chapter 9 sampai terbaru
  komikdl --chapter -3,7,9,10-14,16- https://example.com/manga/judul-komik/   | bisa di tebak, dari awal sampai nomor 3, lalu nomor 7,9,10 sampai 14, dan 16 sampai terakhir
  komikdl --terbaru https://example.com/manga/judul-komik/                    | mendownload dari yang terbaru
  komikdl --periksa https://example.com/judul-komik-chapter-525/              | Memeriksa gambar rusak di chapter 525
  komikdl --periksa --chapter -10,13 https://example.com/manga/judul-komik/   | Memeriksa gambar rusak dari chapter awal ke 10, dan nomor 13
  komikdl --total-chapter https://example.com/judul-komik-chapter-525/        | Mencetak total chapter untuk komik yang dimaksud
  komikdl --total-chapter https://example.com/manga/judul-komik/              | Hasil nya juga sama
  komikdl --chapter 2,3 --pdf https://example.com/manga/judul-komik/          | Mendownload PDF untuk chapter 2 dan 3
  komikdl --input-file "F:\kumpulan_url_komik.txt"                            | Mendownload bedasarkan URL yang ada di file 
```

Untuk parameter `--input-file` sayangnya parameter yang lain tidak akan terpengaruh tetapi parameter lain tersebut
bisa diletakkan disamping URL yang ada di dalam. Sebagai contoh ada di bawah
##### Isi dari file kumpulan_url_komik.txt
```
https://sekt**.com/manga/judul-komik/ 
https://komi**id/manga/judul-komik/ --chapter 300-
https://sekt**.com/judul-komik-chapter-01-bahasa-indonesia/ --pdf
```

Sebagai tambahan, jelas saja banyak kesalahan dan kekurangan dari program ini dikarenakan masih kurang nya pengetahuan yang 
saya miliki dalam membuatnya. Seperti kemungkinan menemukan pesan error dan program tidak berjalan sebagai mestinya.
Tapi yang paling jelas, tidak semua situs komik support dalam program tool ini, dikarenakan belum saya tambahkan 
ataupun memang saya mengalami kendala dalam menangangi situs web tersebut. 

Kumpulan daftar situs web yang dimaksud yang juga kujadikan sebagai modul untuk program tool ini ada di dalam direktori `modules`

