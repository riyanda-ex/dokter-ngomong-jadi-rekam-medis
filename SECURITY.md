# Keamanan

## Jangan Laporkan Data Pasien di Issue Publik
Jangan pernah upload rekaman suara, nama pasien, NIK, atau foto rekam medis ke GitHub Issue.

## Melaporkan Celah Keamanan
Hubungi pemilik repo melalui GitHub (tab Discussions / profil) secara privat.
Jelaskan: file yang bermasalah, langkah reproduksi, dan dampaknya.

## Prinsip
- Data pasien tidak pernah disimpan di repo ini.
- Hanya ID anonim (`PASIEN-001`) dan contoh sintetis yang boleh di-commit.
- File audio (`.wav`, `.mp3`) diblokir oleh `.gitignore`.
