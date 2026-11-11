# Dokter Ngomong Jadi Rekam Medis - V1
# Input: Suara dokter (transkrip teks)
# Output: Rekam Medis rapi + ICD-10 + Resep

import re
from datetime import datetime

class DokterVoiceToEHR:
    def __init__(self):
        # Kamus Jawa + Indonesia + Medis - Ini senjata rahasia kamu yang tidak dipunya Amerika
        self.kamus_gejala = {
            "nggreges": "menggigil / meriang",
            "pilek": "flu / pilek",
            "awak e anget": "demam",
            "anget": "demam",
            "watuk": "batuk",
            "batuk": "batuk",
            "mual": "mual",
            "muntah": "muntah",
            "pusing": "pusing / sakit kepala",
            "ngelu": "pusing / sakit kepala",
            "maag": "nyeri lambung",
            "weteng e lara": "nyeri perut",
            "sesak": "sesak napas",
            "diare": "diare",
            "mencret": "diare",
            "gatel": "gatal",
            "luka": "luka",
        }

        self.kamus_icd10 = {
            "demam": "R50.9",
            "batuk": "R05",
            "flu": "J11.1",
            "pilek": "J00",
            "diare": "A09.9",
            "pusing": "R51",
            "maag": "K29.7",
            "hipertensi": "I10",
            "diabetes": "E11.9",
            "sesak": "R06.02",
            "mual": "R11.0",
        }

        self.kamus_obat = {
            "paracetamol": "Paracetamol 500mg - 3x1",
            "amoxilin": "Amoxicillin 500mg - 3x1",
            "amoxicillin": "Amoxicillin 500mg - 3x1",
            "vitamin": "Vitamin C 500mg - 1x1",
            "obat maag": "Omeprazole 20mg - 1x1 sebelum makan",
        }

    def bersihkan_teks_jawa(self, teks):
        # Ubah bahasa Jawa / gaul jadi bahasa medis formal
        teks_bersih = teks.lower()
        for kata_jawa, arti_medis in self.kamus_gejala.items():
            if kata_jawa in teks_bersih:
                teks_bersih = teks_bersih.replace(kata_jawa, arti_medis)
        return teks_bersih

    def ekstrak_tensi(self, teks):
        # Cari pola 140/90 dari omongan dokter
        match = re.search(r'(\d{2,3})/(\d{2,3})', teks)
        if match:
            return f"{match.group(1)}/{match.group(2)} mmHg"
        return "Tidak tercatat"

    def ekstrak_durasi(self, teks):
        # Cari "3 dino", "3 hari", "2 minggu"
        match = re.search(r'(\d+)\s*(dino|hari|minggu|bulan)', teks)
        if match:
            return f"{match.group(1)} {match.group(2)}"
        return "-"

    def proses_suara_dokter(self, nama_pasien, transkrip_suara):
        print(f"\n=== MENDENGARKAN DOKTER ===")
        print(f"Suara asli: {transkrip_suara}")
        
        teks_bersih = self.bersihkan_teks_jawa(transkrip_suara)
        print(f"Diterjemahkan: {teks_bersih}")

        # Deteksi gejala
        gejala_ditemukan = []
        kode_icd = []
        for gejala, kode in self.kamus_icd10.items():
            if gejala in teks_bersih:
                gejala_ditemukan.append(gejala)
                kode_icd.append(f"{gejala} -> {kode}")

        # Deteksi obat
        resep = []
        for kata_obat, dosis in self.kamus_obat.items():
            if kata_obat in teks_bersih:
                resep.append(dosis)

        # Buat Rekam Medis Rapi
        rekam_medis = {
            "pasien": nama_pasien,
            "tanggal": datetime.now().strftime("%d %B %Y %H:%M"),
            "keluhan_utama": teks_bersih,
            "gejala": gejala_ditemukan,
            "tensi": self.ekstrak_tensi(transkrip_suara),
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
        print(f"Gejala: {', '.join(rm['gejala'])}")
        print(f"Tensi: {rm['tensi']}")
        print(f"Durasi: {rm['durasi_sakit']}")
        print(f"Diagnosa ICD-10: {', '.join(rm['diagnosa_icd10'])}")
        print(f"Resep: {', '.join(rm['resep'])}")
        print("===========================================")
        print(f"HEMAT WAKTU: 10 menit mengetik -> 0 detik")

# CONTOH PAKAI - SIMULASI DOKTER NGOMONG
if __name__ == "__main__":
    dokter_ai = DokterVoiceToEHR()

    # Contoh 1: Dokter di Kediri ngomong campur Jawa
    dokter_ai.proses_suara_dokter(
        "Bu Siti",
        "Pasiene pilek, nggreges, awak e anget 3 dino, tensi 140/90, kasih paracetamol"
    )

    # Contoh 2: Dokter di Jakarta ngomong Indonesia formal
    dokter_ai.proses_suara_dokter(
        "Pak Budi",
        "Pasien batuk 2 minggu, sesak, pusing, tensi 150/95, kasih amoxilin"
    )

    # Contoh 3: Dokter anak
    dokter_ai.proses_suara_dokter(
        "Dek Ani",
        "Anak demam, muntah, mual, diare 2 hari"
    )
