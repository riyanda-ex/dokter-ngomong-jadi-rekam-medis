# Dokter Ngomong Jadi Rekam Medis

Dokter tidak perlu lagi mengetik 10 menit per pasien.

### Masalah
Dokter di Indonesia menghabiskan 70% waktu untuk mengetik, bukan memeriksa pasien. Pasien merasa dicuekin. Dokter kecapekan.

Software luar negeri seperti Nuance DAX harganya Rp 5 juta/bulan dan tidak mengerti Bahasa Jawa / Indonesia campur.

### Solusi
Dokter cukup NGOMONG. Sistem otomatis:
1. Menerjemahkan Bahasa Jawa / Indonesia gaul -> Bahasa Medis formal
2. Mendeteksi gejala, tensi, durasi sakit
3. Memberikan kode ICD-10 otomatis (Standar WHO)
4. Membuat resep otomatis

### Contoh
Input Suara: "Pasiene pilek, nggreges, awak e anget 3 dino, tensi 140/90, kasih paracetamol"
Output: Rekam Medis rapi + ICD-10 R50.9 + Resep Paracetamol 500mg

### Teknologi
- Python
- NLP Kamus Jawa-Indonesia-Medis (200+ kata)
- Regex untuk Tensi & Durasi
- ICD-10 WHO Standard
- Siap integrasi ke Whisper AI / Google Speech-to-Text untuk suara asli

### Keunggulan vs Produk Luar Negeri
- Harga 0 vs Rp 5 juta/bulan
- Mengerti "nggreges", "awak e anget", "weteng e lara"
- Bisa jalan offline di HP klinik kecil

### Roadmap V2
- Rekam suara asli via HP (bukan teks)
- Integrasi langsung ke MediPass Universal
- Deteksi suara 2 bahasa otomatis
