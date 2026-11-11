# Dokter Ngomong Jadi Rekam Medis - V2 FULL
# Input: Suara dokter (transkrip teks)
# Output: Rekam Medis rapi + ICD-10 + Resep
# Kamus diambil dari kamus_jawa.json biar gampang ditambah

import re
import json
import os
from datetime import datetime

class DokterVoiceToEHR:
    def __init__(self):
        # 1. LOAD KAMUS JAWA DARI FILE JSON
        self.kamus_gejala = self.load_kamus()

        # 2. KAMUS ICD-10 WHO Standard
        self.kamus_icd10 = {
            "demam": "R50.9",
            "batuk": "R05",
            "flu": "J11.1",
            "pilek": "J00",
            "diare": "A09.9",
            "pusing": "R51",
            "maag": "K29.7",
            "nyeri lambung": "K29.7",
            "hipertensi": "I10",
            "diabetes": "E11.9",
            "sesak": "R06.02",
            "sesak napas": "R06.02",
            "mual": "R11.0",
            "muntah": "R11.10",
            "nyeri perut": "R10.9",
            "gatal": "L29.9",
            "luka": "S01.9",
            "nyeri tenggorokan": "J02.9",
            "mata merah": "H57.9",
            "mimisan": "R04.0",
            "alergi": "T78.40",
            "sariawan": "K12.0",
            "nyeri pinggang": "M54.5",
            "nyeri otot": "M79.1",
            "asam urat": "M10.9",
            "bengkak": "R60.0",
            "lemas": "R53.1",
        }

        # 3. KAMUS OBAT
        self.kamus_obat = {
            "paracetamol": "Paracetamol 500mg - 3x1",
            "amoxilin": "Amoxicillin 500mg - 3x1",
            "amoxicillin": "Amoxicillin 500mg - 3x1",
            "vitamin": "Vitamin C 500mg - 1x1",
            "obat maag": "Omeprazole 20mg - 1x1 sebelum makan",
            "omeprazole": "Omeprazole 20mg - 1x1 sebelum makan",
            "obat batuk": "Guaifenesin Syrup - 3x1 sendok",
            "obat flu": "Cetirizine 10mg - 1x1",
            "cetirizine": "Cetirizine 10mg - 1x1",
            "oralit": "Oralit - 1 bungkus tiap BAB cair",
        }

    def load_kamus(self):
        # Cari file kamus_jawa.json di folder yang sama
        file_kamus = os.path.join(os.path.dirname(__file__), 'kamus_jawa.json')
        # Kalau file tidak ada, pakai kamus cadangan biar tidak error
        try:
            with open(file_kamus, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Kamus berhasil dimuat: {len(data)} kata Jawa/Indonesia")
                return data
        except FileNotFoundError:
            print("WARNING: kamus_jawa.json tidak ditemukan, pakai kamus cadangan")
            return {
                "nggreges": "menggigil / meriang",
                "awak e anget": "demam",
                "pilek": "flu / pilek",
                "watuk": "batuk",
            }

    def bersihkan_teks_jawa(self, teks):
        # Ubah bahasa Jawa / gaul jadi bahasa medis formal
        # Urutkan dari frasa terpanjang dulu biar "awak e anget" tidak kalah sama "anget"
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

    def proses_suara_dokter(self, nama_pasien, transkrip_suara):
        print(f"\n=== MENDENGARKAN DOKTER ===")
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
            "pasien": nama_pasien,
            "tanggal": datetime.now().strftime("%d %B %Y %H:%M"),
            "keluhan_utama": teks_bersih,
            "gejala": gejala_ditemukan,
            "tensi": self.ekstrak_tensi(transkrip_suara),
            "suhu": self.ekstrak_suhu(transkrip_suara),
            "durasi_sakit": self.ekstrak_durasi(transkrip_suara),
            "diagnosa_icd10": kode_icd,
            "resep": resep if resep else ["Belum ada resep"],
            "status": "Selesai - Otomatis dari suara"
        }

        self.tampilkan_hasil(rekam_medis)
        return rekam_medis

    def tampilkan_hasil(self, rm):
        print("\n========== REKAM MEDIS OTOMATIS ==========")
        print(f"Pasien: {rm['pasien']}")
        print(f"Tanggal: {rm['tanggal']}")
        print(f"Keluhan: {rm['keluhan_utama']}")
        print(f"Gejala: {', '.join(rm['gejala']) if rm['gejala'] else '-'}")
        print(f"Tensi: {rm['tensi']}")
        print(f"Suhu: {rm['suhu']}")
        print(f"Durasi: {rm['durasi_sakit']}")
        print(f"Diagnosa ICD-10: {', '.join(rm['diagnosa_icd10']) if rm['diagnosa_icd10'] else '-'}")
        print(f"Resep: {', '.join(rm['resep'])}")
        print("===========================================")
        print(f"HEMAT WAKTU: 10 menit mengetik -> 0 detik")

# CONTOH PAKAI
if __name__ == "__main__":
    dokter_ai = DokterVoiceToEHR()

    dokter_ai.proses_suara_dokter(
        "Bu Siti",
        "Pasiene pilek, nggreges, awak e anget 3 dino, tensi 140/90, suhu 38.5, kasih paracetamol"
    )

    dokter_ai.proses_suara_dokter(
        "Pak Budi",
        "Pasien batuk 2 minggu, sesak, pusing, boyok e lara, tensi 150/95, kasih amoxilin"
    )

    dokter_ai.proses_suara_dokter(
        "Dek Ani",
        "Anak demam, muntah, mual, mencret 2 hari, kasih oralit"
    )

    dokter_ai.proses_suara_dokter(
        "Mbah Karno",
        "Weteng e lara, mual, ora doyan mangan, darah tinggi, tensi 160/100"
    )
