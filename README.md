# 🩺 Dokter Ngomong Jadi Rekam Medis

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Tests](https://github.com/riyanda-ex/dokter-ngomong-jadi-rekam-medis/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)
![Status](https://img.shields.io/badge/Status-Selesai-green)
![Klinik](https://img.shields.io/badge/Klinik-Al%20Madina%20Husada-teal)

Dokter ngomong (Bahasa Jawa / Indonesia) -> langsung jadi **Rekam Medis rapi + Kode ICD-10 + Resep**.

Dibuat untuk Klinik Al Madina Husada, Nganjuk. Hemat 10 menit mengetik per pasien.

> **Disclaimer Medis:** Sistem ini adalah alat bantu pencatatan, BUKAN pengganti diagnosis dokter. Semua hasil harus diverifikasi oleh dokter sebelum digunakan untuk tindakan medis.

## ✨ Fitur
- Terjemahan Bahasa Jawa Ngoko (Nganjuk) -> Bahasa Medis Formal (90+ kata)
- Ekstrak otomatis: Tensi, Suhu, Durasi Sakit
- Mapping ICD-10 WHO Standard (30+ diagnosis)
- Rekomendasi Resep otomatis
- Simpan laporan JSON ke folder `laporan/` (ID Anonim, tanpa nama asli)
- 10 Test Otomatis

## 🚀 Cara Pakai
```bash
python main.py
# atau
python test.py
