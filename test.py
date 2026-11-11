# Test otomatis untuk DokterVoiceToEHR
# Cara jalanin: python test.py

from main import DokterVoiceToEHR

def test_jawa():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test Jawa", "pasiene nggreges, awak e anget")
    assert "demam" in hasil["keluhan_utama"], "Gagal translate Jawa ke demam"
    print("✅ TEST JAWA LULUS - nggreges -> demam")

def test_tensi():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test Tensi", "tensi 140/90, pilek")
    assert hasil["tensi"] == "140/90 mmHg", f"Tensi salah: {hasil['tensi']}"
    print("✅ TEST TENSI LULUS - 140/90 terbaca")

def test_icd10():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test ICD", "pasien demam, batuk")
    # Harus nemu kode R50.9 untuk demam dan R05 untuk batuk
    kode = " ".join(hasil["diagnosa_icd10"])
    assert "R50.9" in kode, "ICD Demam tidak ketemu"
    assert "R05" in kode, "ICD Batuk tidak ketemu"
    print("✅ TEST ICD-10 LULUS - R50.9 & R05 ketemu")

def test_diare_jawa():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test Diare", "anak mencret 2 hari, kasih oralit")
    assert "diare" in hasil["keluhan_utama"]
    assert "Oralit" in " ".join(hasil["resep"])
    print("✅ TEST DIARE JAWA LULUS - mencret -> diare + oralit")

def test_suhu_durasi():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test Suhu", "awak e anget 3 dino, suhu 38.5")
    assert hasil["durasi_sakit"] == "3 hari", f"Durasi salah: {hasil['durasi_sakit']}"
    assert "38.5" in hasil["suhu"]
    print("✅ TEST SUHU & DURASI LULUS - 3 dino -> 3 hari, 38.5°C")

if __name__ == "__main__":
    print("\n=== JALANIN SEMUA TEST ===")
    test_jawa()
    test_tensi()
    test_icd10()
    test_diare_jawa()
    test_suhu_durasi()
    print("\n🎉 SEMUA 5 TEST LULUS! Repo aman.")
