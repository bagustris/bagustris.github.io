# Gaya selingkung (Style) Repository untuk Tugas Akhir aka Skripsi S1

## Nama Repo
Tugas-Akhir, contoh: [bagustris/Tugas-Akhir](https://github.com/bagustris/Tugas-Akhir)

## Struktur Direktori
- `code`: 
   - berisi coding utama untuk mendapatkan data yang dipakai di buku TA, 
   - coding untuk plot
   - diambil dari hasil terbaik di direktori `exp`
   - hendaknya dibagi per bab berdasarkan buku
- `data`: berisi raw data, baik yang digunakan di `code` atau `exp`. Contoh:  
   - X_si.npy
   - X_sd.npy
   - y_si.npy
   - y_sd.npy
- `figs`: berisi gambar
- `book`: berisi file buku TA: Latex, ms word, atau LibreOffice Writer, Google Doc, dll.
- `exps`: direktori **UTAMA** yang berisi experimen berdasarkan waktu
   - 2021:
      - oktober:  
         - klasifikasi_unbalance_normal.py  
         - klasifikasi_4_kelas.py  
      - november
      - desember
   - 2022:  
      - januari
      - februari
      - maret  
      - april 
      - mei   
      - juni
      - juli
- `notes`:  
  Berisi catatan MINGGUAN dengan format YYYY-MM-DD.md yang berisi:  
  - diskusi dengan dosen pembimbing
  - pertanyan dan jawaban
  - apa yang belum paham (minggu ini)
  - apa yang ingin dipelajari
  - permasalahan
  - temuan
  - dll (*like research diary atau journal*)
- README.md: berisi panduan untuk mereplikasi TA, kontak, promosi, dll.
