# Analisis Data Kesehatan Amazfit Band 3

Analisis data jalan kaki, tidur, dan detak jantung dari Amazfit Band 3, terinspirasi dari artikel blog: https://bagustris.blogspot.com/2021/05/data-jalan-kaki-tidur-dan-detak-jantung.html

## 📊 Ringkasan Data

### Data Langkah Kaki (Activity)
- **Periode**: Mei 2023 - September 2025
- **Total hari tercatat**: 130 hari
- **Rentang tanggal**: 2023-05-10 sampai 2025-09-30

### Data Tidur (Sleep)
- **Periode**: Mei 2023 - September 2025
- **Total malam tercatat**: 110 malam
- **Rentang tanggal**: 2023-05-11 sampai 2025-09-30

### Data Detak Jantung (Heart Rate)
- **Periode**: Mei 2023 - Juli 2025
- **Total pengukuran**: 17 pengukuran
- **Rentang tanggal**: 2023-05-11 sampai 2025-07-19

## 📈 Hasil Visualisasi

Skrip analisis menghasilkan 4 visualisasi utama:

### 1. activity_monthly_stats.png
Menampilkan statistik bulanan untuk:
- Rata-rata langkah per hari
- Rata-rata jarak tempuh (meter)
- Rata-rata kalori terbakar (kcal)

**Temuan Utama:**
- Bulan Juni 2023 memiliki rata-rata langkah tertinggi (7,067 langkah/hari)
- Bulan Agustus 2023 memiliki rata-rata langkah terendah (2,779 langkah/hari)
- Target 8,000 langkah per hari belum tercapai secara konsisten

### 2. sleep_duration_monthly.png
Menampilkan:
- Durasi tidur bulanan (deep sleep + shallow sleep)
- Total waktu tidur dalam jam
- Perbandingan dengan target tidur normal (6-9 jam)

**Temuan Utama:**
- Rata-rata durasi tidur berkisar antara 5.5 - 7.3 jam per malam
- Bulan Juli 2025 memiliki durasi tidur terpanjang (7.3 jam)
- Bulan Agustus 2025 memiliki durasi tidur terpendek (5.5 jam)
- Sebagian besar malam masih dalam rentang tidur normal (6-9 jam)

### 3. sleep_wake_times.png
Menampilkan:
- Rata-rata jam tidur (bed time)
- Rata-rata jam bangun (wake time)

**Temuan Utama:**
- Waktu tidur cukup konsisten, rata-rata sekitar pukul 14:00-16:00 (jam sistem UTC)
- Waktu bangun bervariasi antara pukul 14:46-22:17

### 4. heartrate_analysis.png
Menampilkan:
- Distribusi detak jantung
- Box plot statistik detak jantung
- Time series detak jantung
- Statistik lengkap (mean, median, mode, dll.)

**Temuan Utama:**
- **Mean**: 80.82 BPM
- **Median**: 82 BPM
- **Mode**: 63 BPM
- **Range**: 58-102 BPM
- Detak jantung berada dalam rentang normal untuk aktivitas sehari-hari

## 🚀 Cara Menggunakan

### Prasyarat
```bash
pip install pandas matplotlib seaborn numpy
```

### Menjalankan Analisis
```bash
python3 analyze_health_data.py
```

### Output
- 4 file gambar PNG dengan resolusi tinggi (300 DPI)
- Statistik tercetak di terminal/console

## 📊 Statistik Bulanan Detail

### Langkah Kaki
| Bulan | Langkah (avg) | Jarak (m) | Kalori (kcal) |
|-------|---------------|-----------|---------------|
| 2023-05 | 3,624 | 2,407 | 128 |
| 2023-06 | 7,067 | 4,879 | 225 |
| 2023-07 | 3,648 | 2,445 | 156 |
| 2023-08 | 2,779 | 1,832 | 112 |
| 2025-07 | 6,091 | 4,293 | 97 |
| 2025-08 | 5,247 | 3,716 | 98 |
| 2025-09 | 5,276 | 3,739 | 170 |

### Waktu Tidur
| Bulan | Deep (min) | Shallow (min) | Total (jam) | Bed Time | Wake Time |
|-------|------------|---------------|-------------|----------|-----------|
| 2023-05 | 102 | 285 | 6.9 | 14:01 | 22:17 |
| 2023-06 | 52 | 300 | 6.5 | 15:54 | 14:46 |
| 2023-07 | 58 | 256 | 5.9 | 14:57 | 21:10 |
| 2023-08 | 64 | 313 | 6.9 | 14:29 | 21:06 |
| 2025-07 | 61 | 303 | 7.3 | 13:59 | 21:56 |
| 2025-08 | 46 | 217 | 5.5 | 14:28 | 20:26 |
| 2025-09 | 77 | 207 | 6.1 | 15:55 | 22:03 |

### Detak Jantung
| Statistik | Nilai |
|-----------|-------|
| Mean | 80.82 BPM |
| Standard Deviation | 14.29 BPM |
| Median | 82 BPM |
| Mode | 63 BPM |
| Min | 58 BPM |
| Max | 102 BPM |
| Q1 (25%) | 70 BPM |
| Q3 (75%) | 93 BPM |

## 💡 Rekomendasi

### Aktivitas Fisik
- **Target**: Tingkatkan konsistensi untuk mencapai minimal 8,000 langkah per hari
- **Observasi**: Juni 2023 menunjukkan performa terbaik, pertimbangkan faktor-faktor yang mempengaruhi bulan tersebut
- **Saran**: Jadwalkan aktivitas rutin seperti jalan pagi/sore

### Kualitas Tidur
- **Positif**: Mayoritas malam memenuhi target 6-9 jam tidur
- **Perhatian**: Beberapa bulan menunjukkan deep sleep yang relatif rendah
- **Saran**: 
  - Pertahankan konsistensi waktu tidur
  - Tingkatkan kualitas deep sleep dengan mengurangi gangguan sebelum tidur
  - Hindari penggunaan gadget 1 jam sebelum tidur

### Detak Jantung
- **Status**: Detak jantung dalam rentang normal
- **Observasi**: Variasi detak jantung menunjukkan aktivitas yang beragam
- **Saran**: Lanjutkan monitoring untuk mendeteksi anomali

## 📝 Catatan

- Data menggunakan format waktu UTC+0000
- Hari dengan langkah = 0 dianggap sebagai hari perangkat tidak dipakai (excluded)
- Malam dengan total tidur = 0 dianggap tidak valid (excluded)
- Detak jantung di luar rentang 40-200 BPM dianggap outlier (excluded)

## 🔗 Referensi

- Blog Post: [Data Jalan Kaki, Tidur, dan Detak Jantung](https://bagustris.blogspot.com/2021/05/data-jalan-kaki-tidur-dan-detak-jantung.html)
- Device: Amazfit Band 3
- Data Export: Zepp App

## 📄 Lisensi

Data pribadi untuk analisis dan pembelajaran.

---

**Terakhir diperbarui**: 7 Januari 2026
