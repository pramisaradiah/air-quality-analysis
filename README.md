# Proyek Analisis Data: Air Quality Dataset

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis kualitas udara di Beijing berdasarkan konsentrasi PM2.5 selama periode Maret 2013 hingga Februari 2017. Analisis dilakukan menggunakan data dari 12 stasiun pemantauan kualitas udara.

Melalui proyek ini, dilakukan proses pengumpulan data, penilaian kualitas data, pembersihan data, eksplorasi data (Exploratory Data Analysis), visualisasi, serta analisis lanjutan untuk memperoleh informasi mengenai pola konsentrasi PM2.5.

Hasil analisis kemudian disajikan melalui dashboard interaktif menggunakan Streamlit agar informasi dapat dipahami dengan lebih mudah.

## Dataset

Dataset yang digunakan adalah **Beijing Multi-Site Air Quality Dataset**, yang terdiri dari 12 file CSV dari masing-masing stasiun pemantauan kualitas udara di Beijing.

Informasi dataset:
- Lokasi pengamatan: Beijing, China.
- Periode pengamatan: Maret 2013 – Februari 2017.
- Jumlah stasiun pemantauan: 12 stasiun.
- Jumlah data gabungan: 420.768 baris.
- Variabel yang dianalisis meliputi PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, dan WSPM.

## Pertanyaan Analisis

Proyek ini berfokus pada empat pertanyaan utama:

1. Bagaimana perubahan rata-rata konsentrasi PM2.5 setiap bulan selama periode Maret 2013 hingga Februari 2017, dan pada periode kapan konsentrasi PM2.5 mencapai tingkat tertinggi?
2. Stasiun pemantauan mana yang memiliki rata-rata konsentrasi PM2.5 tertinggi dan terendah selama periode Maret 2013 hingga Februari 2017?
3. Bagaimana hubungan antara faktor meteorologi, seperti suhu (TEMP), tekanan udara (PRES), titik embun (DEWP), curah hujan (RAIN), dan kecepatan angin (WSPM), dengan konsentrasi PM2.5 selama periode Maret 2013 hingga Februari 2017?
4. Bagaimana perbedaan rata-rata konsentrasi PM2.5 pada empat musim, yaitu semi, panas, gugur, dan dingin?

## Tahapan Analisis

Tahapan yang dilakukan dalam proyek ini meliputi:

1. **Data Gathering:** Mengumpulkan dan menggabungkan data dari 12 stasiun pemantauan.
2. **Data Assessing:** Memeriksa kualitas data, seperti tipe data, missing values, duplikasi, dan nilai yang tidak sesuai.
3. **Data Cleaning:** Menangani missing values dan memperbaiki kualitas data agar dapat digunakan dalam analisis.
4. **Exploratory Data Analysis (EDA):** Mengeksplorasi distribusi data, tren bulanan PM2.5, perbedaan antarstasiun, serta hubungan dengan faktor meteorologi.
5. **Visualization & Explanatory Analysis:** Menyajikan hasil analisis melalui grafik dan visualisasi yang menjawab pertanyaan analisis.
6. **Analisis Lanjutan:** Membandingkan rata-rata konsentrasi PM2.5 berdasarkan empat musim.

## Struktur Folder

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
│   ├── PRSA_Data_Changping_20130301-20170228.csv
│   ├── PRSA_Data_Dingling_20130301-20170228.csv
│   ├── PRSA_Data_Dongsi_20130301-20170228.csv
│   ├── PRSA_Data_Guanyuan_20130301-20170228.csv
│   ├── PRSA_Data_Gucheng_20130301-20170228.csv
│   ├── PRSA_Data_Huairou_20130301-20170228.csv
│   ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
│   ├── PRSA_Data_Shunyi_20130301-20170228.csv
│   ├── PRSA_Data_Tiantan_20130301-20170228.csv
│   ├── PRSA_Data_Wanliu_20130301-20170228.csvv
│   └── PRSA_Data_Wanshouxigong_20130301-20170228.csv
├── notebook.ipynb
├── README.md
└── requirements.txt
```

## Instalasi dan Persiapan

Pastikan Python sudah terinstal pada komputer.

1. Buka folder proyek `submission` menggunakan Visual Studio Code.
2. Buka terminal pada folder tersebut.
3. Instal seluruh library yang dibutuhkan menggunakan perintah:

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook

Notebook analisis dapat dijalankan menggunakan Jupyter Notebook atau Google Colab.

Pastikan folder `data` yang berisi 12 file CSV tersedia pada direktori kerja notebook agar proses pengumpulan data dapat berjalan dengan baik.

Jalankan seluruh cell notebook secara berurutan mulai dari bagian import packages hingga conclusion and recommendation.

## Menjalankan Dashboard

Dashboard dibuat menggunakan Streamlit dan Plotly.

Pastikan file `main_data.csv` berada di dalam folder `dashboard` bersama dengan file `dashboard.py`.

Jalankan perintah berikut melalui terminal dari folder utama `submission`:

```bash
python -m streamlit run dashboard/dashboard.py
```

Setelah berhasil dijalankan, dashboard dapat diakses melalui browser pada alamat:

```text
http://localhost:8501
```

## Fitur Dashboard

Dashboard menyediakan beberapa fitur untuk membantu pengguna memahami hasil analisis, yaitu:

- Filter stasiun pemantauan.
- Filter periode pengamatan.
- Ringkasan statistik konsentrasi PM2.5.
- Visualisasi tren rata-rata PM2.5 bulanan.
- Visualisasi perbandingan rata-rata PM2.5 antarstasiun.
- Heatmap korelasi PM2.5 dengan faktor meteorologi.
- Visualisasi perbandingan rata-rata PM2.5 berdasarkan empat musim.
- Tabel data dan fitur unduh dataset berdasarkan filter.

## Teknologi dan Library

Teknologi dan library yang digunakan dalam proyek ini meliputi:

- **Python:** Bahasa pemrograman untuk pengolahan dan analisis data.
- **Pandas:** Mengolah dan memanipulasi dataset.
- **NumPy:** Mendukung operasi numerik.
- **Matplotlib dan Seaborn:** Membantu visualisasi data pada notebook.
- **Plotly:** Membuat visualisasi interaktif pada dashboard.
- **Streamlit:** Membangun dashboard interaktif.
- **Google Colab / Jupyter Notebook:** Menjalankan proses analisis data.

## Kesimpulan

Proyek ini menghasilkan analisis mengenai pola konsentrasi PM2.5 di Beijing berdasarkan perubahan bulanan, perbedaan antarstasiun pemantauan, hubungan dengan faktor meteorologi, serta perbedaan berdasarkan musim.

Dashboard interaktif dikembangkan untuk memudahkan pengguna dalam mengeksplorasi hasil analisis melalui berbagai visualisasi dan filter data.