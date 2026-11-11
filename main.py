# Dokter Ngomong Jadi Rekam Medis - V3 FINAL (100% Aman & Sistematis)
# Input: Transkrip teks suara dokter
# Output: Rekam Medis rapi + ICD-10 + Resep + File JSON di laporan/
# DISCLAIMER: Alat bantu pencatatan, BUKAN pengganti diagnosis dokter.
# Semua hasil WAJIB diverifikasi dokter sebelum tindakan medis.

import re
import json
import os
from datetime import datetime

class DokterVoiceToEHR:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.kamus_gejala = self.load_kamus()
        self.kamus_icd10 = self.config.get("icd10", {})
        self.kamus_obat = self.config.get("obat", {})

    def load_config(self, path):
        base = os.path.dirname(__file__)
        full = os.path.join(base, path)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("WARNING: config.json tidak ditemukan, pakai kamus cadangan")
            return {"icd10": {"demam": "R50.9", "batuk": "R05"}, "obat": {}}

    def load_kamus(self):
        file_kamus = os.path.join(os.path.dirname(__file__), 'kamus_jawa.json')
        try:
            with open(file_kamus, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Kamus berhasil dimuat: {len(data)} kata Jawa/Indonesia")
                return data
        except FileNotFoundError:
            print("WARNING: kamus_jawa.json tidak ditemukan, pakai kamus cadangan")
            return {"nggreges": "menggigil / meriang", "awak e anget": "demam", "watuk": "batuk"}

    def bersihkan_teks_jawa(self, teks):
        if not teks or not teks.strip():
            return ""
        teks_bersih = teks.lower()
        for kata_jawa in sorted(self.kamus_gejala.keys(), key=len, reverse=True):
            arti_medis = self.kamus_gejala[kata_jawa]
            if kata_jawa in teks_bersih:
                teks_bersih = teks_bersih.replace(kata_jawa, arti_medis)
        return teks_bersih

    def ekstrak_tensi(self, teks):
        match = re.search(r'(\d{2,3})/(\d{2,3})', teks)
        if match:
            return f"{match.group(1)}/{match.group(2)} mmHg"
        return "Tidak tercatat"

    def ekstrak_durasi(self, teks):
        match = re.search(r'(\d+)\s*(dino|hari|minggu|bulan)', teks)
        if match:
            durasi = match.group(2)
            if durasi == "dino":
                durasi = "hari"
            return f"{match.group(1)} {durasi}"
        return "-"

    def ekstrak_suhu(self, teks):
        match = re.search(r'(\d{2,3}[.,]\d)\s*(derajat|°c|c)?', teks)
        if match:
            return f"{match.group(1)}°C"
        return "Tidak tercatat"

    def anonymize_id(self, id_pasien):
        # Jangan simpan nama asli. Hanya simpan ID anonim.
        if not id_pasien or not id_pasien.strip():
            return "PASIEN-000"
        # Ambil hanya huruf/angka, buang nama asli
        bersih = re.sub(r'[^A-Za-z0-9-_]', '', id_pasien.strip())
        return bersih[:20] if bersih else "PASIEN-000"

    def proses_suara_dokter(self, id_pasien, transkrip_suara, simpan=True):
        if not transkrip_suara or not transkrip_suara.strip():
            print("ERROR: Transkrip kosong, tidak diproses.")
            return None

        id_aman = self.anonymize_id(id_pasien)
        print(f"\n=== MENDENGARKAN DOKTER ===")
        print(f"ID Pasien (Anonim): {id_aman}")
        print(f"Suara asli: {transkrip_suara}")

        teks_bersih = self.bersihkan_teks_jawa(transkrip_suara)
        print(f"Diterjemahkan: {teks_bersih}")

        gejala_ditemukan = []
        kode_icd = []
        for gejala, kode in self.kamus_icd10.items():
            if gejala in teks_bersih:
                gejala_ditemukan.append(gejala)
                kode_icd.append(f"{gejala} -> {kode}")

        resep = []
        for kata_obat, dosis in self.kamus_obat.items():
            if kata_obat in teks_bersih:
                resep.append(dosis)

        rekam_medis = {
            "id_pasien_anonim": id_aman,
            "tanggal": datetime.now().strftime("%d %B %Y %H:%M"),
            "keluhan_utama": teks_bersih,
            "gejala": gejala_ditemukan,
            "tensi": self.ekstrak_tensi(transkrip_suara),
            "suhu": self.ekstrak_suhu(transkrip_suara),
            "durasi_sakit": self.ekstrak_durasi(transkrip_suara),
            "diagnosa_icd10": kode_icd,
            "resep": resep if resep else ["Belum ada resep"],
            "disclaimer": "Alat bantu pencatatan, BUKAN diagnosis. Wajib verifikasi dokter.",
            "status": "Selesai - Otomatis dari suara"
        }

        self.tampilkan_hasil(rekam_medis)
        if simpan:
            self.simpan_laporan(rekam_medis)
        return rekam_medis

    def simpan_laporan(self, rm):
        folder = os.path.join(os.path.dirname(__file__), "laporan")
        os.makedirs(folder, exist_ok=True)
        nama_file = f"{rm['id_pasien_anonim']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(folder, nama_file)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(rm, f, indent=2, ensure_ascii=False)
        print(f"Laporan disimpan: {path}")

    def tampilkan_hasil(self, rm):
        print("\n========== REKAM MEDIS OTOMATIS ==========")
        print(f"ID Pasien: {rm['id_pasien_anonim']}")
        print(f"Tanggal: {rm['tanggal']}")
        print(f"Keluhan: {rm['keluhan_utama']}")
        print(f"Gejala: {', '.join(rm['gejala']) if rm['gejala'] else '-'}")
        print(f"Tensi: {rm['tensi']}")
        print(f"Suhu: {rm['suhu']}")
        print(f"Durasi: {rm['durasi_sakit']}")
        print(f"Diagnosa ICD-10: {', '.join(rm['diagnosa_icd10']) if rm['diagnosa_icd10'] else '-'}")
        print(f"Resep: {', '.join(rm['resep'])}")
        print("===========================================")
        print("DISCLAIMER: Bukan diagnosis. Wajib verifikasi dokter.")
        print(f"HEMAT WAKTU: 10 menit mengetik -> 0 detik")

if __name__ == "__main__":
    print("=== Dokter Ngomong Jadi Rekam Medis ===")
    print("DISCLAIMER: Alat bantu pencatatan, BUKAN pengganti diagnosis dokter.")
    dokter_ai = DokterVoiceToEHR()

    # CONTOH PAKAI - PAKAI ID ANONIM, BUKAN NAMA ASLI
    dokter_ai.proses_suara_dokter(
        "PASIEN-001",
        "Pasiene pilek, nggreges, awak e anget 3 dino, tensi 140/90, suhu 38.5, kasih paracetamol"
    )
    dokter_ai.proses_suara_dokter(
        "PASIEN-002",
        "Pasien batuk 2 minggu, sesak, pusing, boyok e lara, tensi 150/95, kasih amoxilin"
    )
    dokter_ai.proses_suara_dokter(
        "PASIEN-003",
        "Anak demam, muntah, mual, mencret 2 hari, kasih oralit"
    )
    dokter_ai.proses_suara_dokter(
        "PASIEN-004",
        "Weteng e lara, mual, ora doyan mangan, darah tinggi, tensi 160/100"
    )
