import streamlit as st
import pandas as pd
import os
import uuid
from datetime import date

class ManajemenReservasi:
    def __init__(self, nama_file="data_reservasi_ruangan.csv"):
        self.nama_file = nama_file
        self.kolom = ["ID_Reservasi", "Nama_Pemesan", "Kontak", "Ruangan", "Tanggal_Mulai", "Jam_Mulai", "Tanggal_Selesai", "Jam_Selesai", "Alasan_Reservasi"]
        self.buat_file_jika_kosong()

    def buat_file_jika_kosong(self):
        if not os.path.exists(self.nama_file):
            df = pd.DataFrame(columns=self.kolom)
            df.to_csv(self.nama_file, index=False)

    def tambah_data(self, nama, kontak, ruangan, tgl_mulai, jam_mulai, tgl_selesai, jam_selesai, alasan):
        df = pd.read_csv(self.nama_file)
        id_baru = str(uuid.uuid4())[:6].upper()
        data_baru = pd.DataFrame([{
            "ID_Reservasi": id_baru,
            "Nama_Pemesan": nama,
            "Kontak": kontak,
            "Ruangan": ruangan,
            "Tanggal_Mulai": str(tgl_mulai),
            "Jam_Mulai": jam_mulai,
            "Tanggal_Selesai": str(tgl_selesai),
            "Jam_Selesai": jam_selesai,
            "Alasan_Reservasi": alasan
        }])
        df = pd.concat([df, data_baru], ignore_index=True)
        df.to_csv(self.nama_file, index=False)
        return id_baru

    def baca_data(self):
        return pd.read_csv(self.nama_file)

    def perbarui_data(self, id_reservasi, nama_baru, kontak_baru, ruangan_baru, mulai_baru, jam_m_baru, selesai_baru, jam_s_baru, alasan_baru):
        df = pd.read_csv(self.nama_file)
        indeks = df.index[df['ID_Reservasi'] == id_reservasi].tolist()
        if indeks:
            idx = indeks[0]
            df.at[idx, 'Nama_Pemesan'] = nama_baru
            df.at[idx, 'Kontak'] = kontak_baru
            df.at[idx, 'Ruangan'] = ruangan_baru
            df.at[idx, 'Tanggal_Mulai'] = str(mulai_baru)
            df.at[idx, 'Jam_Mulai'] = jam_m_baru
            df.at[idx, 'Tanggal_Selesai'] = str(selesai_baru)
            df.at[idx, 'Jam_Selesai'] = jam_s_baru
            df.at[idx, 'Alasan_Reservasi'] = alasan_baru
            df.to_csv(self.nama_file, index=False)
            return True
        return False

    def hapus_data(self, id_reservasi):
        df = pd.read_csv(self.nama_file)
        df = df[df['ID_Reservasi'] != id_reservasi]
        df.to_csv(self.nama_file, index=False)

st.set_page_config(page_title="PBO ASSIGNMENT", page_icon="🏫", layout="wide")
st.title("🏫 Sistem Reservasi Ruangan Kampus")
st.write("Aplikasi ini memungkinkan pengguna untuk melakukan manajemen reservasi ruangan kampus dengan fitur CRUD (Create, Read, Update, Delete).")

db = ManajemenReservasi()

tab_tambah, tab_lihat, tab_ubah, tab_hapus = st.tabs([
    "➕ Reservasi Baru", 
    "📖 Lihat & Cari Ruangan", 
    "✏️ Edit Reservasi", 
    "🗑️ Hapus Reservasi"
])

pilihan_ruangan = ["Reguler (15 orang)", "Reguler + (25 orang)", "Ruang Rapat (10 orang)", "Ruang Rapat Executive (5 orang)", "Aula (50 orang)"]

pilihan_jam = []
for h in range(7, 22):
    pilihan_jam.extend([f"{h:02d}:00", f"{h:02d}:30"])

with tab_tambah:
    st.header("Tambah Reservasi Baru")
    with st.form("form_tambah"):
        nama = st.text_input("Nama Pemesan / Organisasi")
        kontak = st.text_input("Nomor Telepon / Email")
        ruangan = st.selectbox("Pilih Ruangan", pilihan_ruangan)
        
        col1, col2 = st.columns(2)
        with col1:
            in_date = st.date_input("Tanggal Mulai Pinjam")
            in_time = st.selectbox("Jam Mulai", pilihan_jam, index=0)
        with col2:
            out_date = st.date_input("Tanggal Selesai Pinjam")
            out_time = st.selectbox("Jam Selesai", pilihan_jam, index=4) 
            
        alasan = st.text_area("Alasan Reservasi (Misal: Rapat Organisasi, Kuliah Pengganti, dll)")
            
        submit_tambah = st.form_submit_button("Simpan Reservasi")
        
        if submit_tambah:
            if nama.strip() == "":
                st.error("Nama pemesan harus diisi!")
            elif kontak.strip() == "":
                st.error("Kontak (No. Telepon / Email) harus diisi!")
            elif alasan.strip() == "":
                st.error("Alasan reservasi harus diisi!")
            elif out_date < in_date:
                st.error("Tanggal selesai pinjam tidak boleh sebelum tanggal mulai!")
            elif out_date == in_date and out_time <= in_time:
                st.error("Jam selesai pinjam harus setelah jam mulai!")
            else:
                id_reservasi = db.tambah_data(nama, kontak, ruangan, in_date, in_time, out_date, out_time, alasan)
                st.success(f"Berhasil! Reservasi ruangan disimpan dengan ID: {id_reservasi}")

with tab_lihat:
    st.header("Daftar Reservasi Ruangan")
    df_tampil = db.baca_data()
    
    kata_kunci = st.text_input("Cari berdasarkan Nama Pemesan, Kontak, ID Reservasi, atau Alasan:")
    
    if not df_tampil.empty:
        if kata_kunci:
            df_tampil = df_tampil[
                df_tampil['Nama_Pemesan'].str.contains(kata_kunci, case=False, na=False) |
                df_tampil['Kontak'].str.contains(kata_kunci, case=False, na=False) |
                df_tampil['ID_Reservasi'].str.contains(kata_kunci, case=False, na=False) |
                df_tampil['Alasan_Reservasi'].str.contains(kata_kunci, case=False, na=False)
            ]
        st.dataframe(df_tampil, use_container_width=True)
    else:
        st.info("Belum ada data reservasi ruangan.")

with tab_ubah:
    st.header("Perbarui Data Reservasi")
    df_update = db.baca_data()
    
    if not df_update.empty:
        id_pilihan = st.selectbox("Pilih ID Reservasi yang akan diubah:", df_update['ID_Reservasi'].tolist())
        data_lama = df_update[df_update['ID_Reservasi'] == id_pilihan].iloc[0]
        
        with st.form("form_ubah"):
            nama_u = st.text_input("Nama Pemesan / Organisasi", value=data_lama['Nama_Pemesan'])
            kontak_u = st.text_input("Nomor Telepon / Email", value=data_lama.get('Kontak', ''))
            
            try:
                idx_ruangan = pilihan_ruangan.index(data_lama['Ruangan'])
            except ValueError:
                idx_ruangan = 0
            ruangan_u = st.selectbox("Pilih Ruangan", pilihan_ruangan, index=idx_ruangan)
            
            col1, col2 = st.columns(2)
            with col1:
                tgl_in = pd.to_datetime(data_lama['Tanggal_Mulai']).date()
                in_u = st.date_input("Tanggal Mulai (Baru)", value=tgl_in)
                
                jam_lama_in = str(data_lama['Jam_Mulai'])[:5]
                try:
                    idx_jam_in = pilihan_jam.index(jam_lama_in)
                except ValueError:
                    idx_jam_in = 0
                time_in_u = st.selectbox("Jam Mulai (Baru)", pilihan_jam, index=idx_jam_in)
                
            with col2:
                tgl_out = pd.to_datetime(data_lama['Tanggal_Selesai']).date()
                out_u = st.date_input("Tanggal Selesai (Baru)", value=tgl_out)
                
                jam_lama_out = str(data_lama['Jam_Selesai'])[:5]
                try:
                    idx_jam_out = pilihan_jam.index(jam_lama_out)
                except ValueError:
                    idx_jam_out = 4
                time_out_u = st.selectbox("Jam Selesai (Baru)", pilihan_jam, index=idx_jam_out)
                
            alasan_u = st.text_area("Alasan Reservasi (Baru)", value=data_lama.get('Alasan_Reservasi', ''))
                
            submit_ubah = st.form_submit_button("Simpan Perubahan")
            
            if submit_ubah:
                if nama_u.strip() == "":
                    st.error("Nama pemesan tidak boleh kosong!")
                elif kontak_u.strip() == "":
                    st.error("Kontak (No. Telepon / Email) tidak boleh kosong!")
                elif alasan_u.strip() == "":
                    st.error("Alasan reservasi tidak boleh kosong!")
                elif out_u < in_u:
                    st.error("Tanggal selesai pinjam tidak boleh sebelum tanggal mulai!")
                elif out_u == in_u and time_out_u <= time_in_u:
                    st.error("Jam selesai pinjam harus setelah jam mulai!")
                else:
                    db.perbarui_data(id_pilihan, nama_u, kontak_u, ruangan_u, in_u, time_in_u, out_u, time_out_u, alasan_u)
                    st.success(f"Data reservasi dengan ID {id_pilihan} berhasil diperbarui!")
                    st.rerun()
    else:
        st.info("Tidak ada data reservasi untuk diubah.")

with tab_hapus:
    st.header("Hapus Data Reservasi")
    df_hapus = db.baca_data()
    
    if not df_hapus.empty:
        id_hapus = st.selectbox("Pilih ID Reservasi yang akan dihapus:", df_hapus['ID_Reservasi'].tolist())
        if st.button("Hapus Data Permanen", type="primary"):
            db.hapus_data(id_hapus)
            st.success(f"Data reservasi dengan ID {id_hapus} berhasil dihapus dari sistem.")
            st.rerun()
    else:
        st.info("Tidak ada data reservasi untuk dihapus.")