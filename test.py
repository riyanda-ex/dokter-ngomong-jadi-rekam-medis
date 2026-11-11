# Test otomatis - Dokter Ngomong Jadi Rekam Medis
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from main import DokterVoiceToEHR

def test(nama, kondisi):
    print(f"{'✅' if kondisi else '❌'} {nama}")
    return kondisi

if __name__ == "__main__":
    print("=== TEST Dokter Ngomong Jadi Rekam Medis ===\n")
    d = DokterVoiceToEHR()
    hasil = []

    # 1. Kamus Jawa terload
    hasil.append(test("1. Kamus Jawa terload > 50 kata", len(d.kamus_gejala) >= 50))
    # 2. Terjemahan Jawa
    t = d.bersihkan_teks_jawa("nggreges, awak e anget, watuk")
    hasil.append(test("2. Terjemahan Jawa -> Indonesia", "demam" in t and "batuk" in t))
    # 3. Ekstrak tensi
    hasil.append(test("3. Ekstrak tensi 140/90", d.ekstrak_tensi("tensi 140/90") == "140/90 mmHg"))
    # 4. Ekstrak suhu
    hasil.append(test("4. Ekstrak suhu 38.5", "38.5" in d.ekstrak_suhu("suhu 38.5")))
    # 5. Ekstrak durasi dino -> hari
    hasil.append(test("5. Durasi 3 dino -> 3 hari", d.ekstrak_durasi("sakit 3 dino") == "3 hari"))
    # 6. ICD-10 ketemu
    r = d.proses_suara_dokter("PASIEN-TEST", "demam, batuk, pilek, kasih paracetamol", simpan=False)
    hasil.append(test("6. ICD-10 + Resep ketemu", len(r["diagnosa_icd10"]) >= 2 and "Paracetamol" in str(r["resep"])))
    # 7. Input kosong ditolak
    r2 = d.proses_suara_dokter("PASIEN-TEST", "   ", simpan=False)
    hasil.append(test("7. Input kosong ditolak (return None)", r2 is None))
    # 8. Anonimisasi ID - nama asli tidak disimpan mentah
    r3 = d.proses_suara_dokter("Bu Siti!!!", "demam", simpan=False)
    hasil.append(test("8. ID dianonimkan, tanpa spasi/simbol", " " not in r3["id_pasien_anonim"] and "!" not in r3["id_pasien_anonim"]))
    # 9. Disclaimer ada
    hasil.append(test("9. Disclaimer medis ada", "verifikasi" in r["disclaimer"].lower()))
    # 10. Config terload
    hasil.append(test("10. Config ICD-10 terload", "demam" in d.kamus_icd10))

    lulus = sum(hasil)
    print(f"\nHASIL: {lulus}/{len(hasil)} lulus")
    if lulus == len(hasil):
        print("🎉 SEMUA TEST LULUS!")
    else:
        print("⚠️ Ada test gagal, cek di atas.")
        sys.exit(1)
