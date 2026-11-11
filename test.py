from main import DokterVoiceToEHR

def test_jawa():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test", "pasiene nggreges, awak e anget")
    assert "demam" in hasil["keluhan_utama"]
    print("TEST JAWA LULUS ✅")

def test_tensi():
    dokter = DokterVoiceToEHR()
    hasil = dokter.proses_suara_dokter("Test", "tensi 140/90")
    assert hasil["tensi"] == "140/90 mmHg"
    print("TEST TENSI LULUS ✅")

test_jawa()
test_tensi()
