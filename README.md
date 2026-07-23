# 🏫 Sistem Reservasi Ruangan Kampus

Aplikasi berbasis web sederhana untuk manajemen reservasi ruangan kampus, dibangun menggunakan **Python** dan **Streamlit**. Projek ini mengimplementasikan konsep *Object-Oriented Programming* (OOP) untuk mengelola data peminjaman ruangan dengan sistem penyimpanan berbasis file CSV.

## ✨ Fitur

Aplikasi ini dibagi menjadi 4 tab utama:
1. **➕ Reservasi Baru:** Mengisi formulir peminjaman ruangan yang mencakup Nama, Kontak (Nomor Telepon/Email), Pilihan Ruangan, Tanggal & Jam (menggunakan sistem *dropdown* interval 30 menit), serta note alasan peminjaman.
2. **📖 Lihat & Cari Ruangan:** Menampilkan seluruh data reservasi dalam bentuk tabel interaktif. Dilengkapi dengan fitur **Pencarian** berdasarkan Nama, Kontak, ID Reservasi, atau Alasan.
3. **✏️ Edit Reservasi:** Memperbarui data peminjaman yang sudah ada menggunakan ID Reservasi.
4. **🗑️ Hapus Reservasi:** Menghapus data reservasi secara permanen dari sistem.

## 🛠️ Prasyarat

Pastikan kamu sudah menginstal library berikut di Python kamu:
- `streamlit`
- `pandas`

Kamu bisa menginstalnya sekaligus dengan perintah:
```bash
pip install streamlit pandas