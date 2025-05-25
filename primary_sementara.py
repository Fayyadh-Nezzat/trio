import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

daftar_produk = []
keranjang_belanja = []
produk_sedang_diedit = None

def cari_produk(nama, data):
    ditemukan = -1
    posisi = 0
    while posisi < len(data):
        if data[posisi]['nama'] == nama:
            ditemukan = posisi
            break
        posisi += 1
    return ditemukan

def urutkan_produk(data, kriteria, arah):
    panjang = len(data)
    i = 1
    while i < panjang:
        produk = data[i]
        j = i - 1
        
        if arah == 'naik':
            if kriteria == 'harga':
                while j >= 0 and produk['harga'] < data[j]['harga']:
                    data[j+1] = data[j]
                    j -= 1
            else:
                while j >= 0 and produk['nama'] < data[j]['nama']:
                    data[j+1] = data[j]
                    j -= 1
        else:
            if kriteria == 'harga':
                while j >= 0 and produk['harga'] > data[j]['harga']:
                    data[j+1] = data[j]
                    j -= 1
            else:
                while j >= 0 and produk['nama'] > data[j]['nama']:
                    data[j+1] = data[j]
                    j -= 1
        
        data[j+1] = produk
        i += 1

def segarkan_tampilan_penjual():
    for item in tabel_penjual.get_children():
        tabel_penjual.delete(item)
    
    tampilkan = list(daftar_produk)
    
    if input_cari_penjual.get():
        hasil_cari = []
        for produk in tampilkan:
            if input_cari_penjual.get().lower() in produk['nama'].lower():
                hasil_cari.append(produk)
        tampilkan = hasil_cari
    
    urutkan_produk(tampilkan, pilihan_kriteria.get().lower(), pilihan_urutan.get().lower())
    
    for produk in tampilkan:
        tabel_penjual.insert("", "end", values=(produk['nama'], f"Rp{produk['harga']:,}", produk['stok']))

def tambah_edit_produk():
    global produk_sedang_diedit
    
    nama = input_nama.get()
    harga = input_harga.get()
    stok = input_stok.get()
    
    if not nama or not harga or not stok:
        messagebox.showerror("Error", "Harap isi semua kolom!")
        return
    
    try:
        harga = int(harga)
        stok = int(stok)
        if harga <= 0 or stok < 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Harga dan stok harus angka positif!")
        return
    
    if produk_sedang_diedit:
        indeks = cari_produk(produk_sedang_diedit, daftar_produk)
        if indeks != -1:
            if nama != produk_sedang_diedit:
                if cari_produk(nama, daftar_produk) != -1:
                    messagebox.showerror("Error", "Nama produk sudah ada!")
                    return
            
            daftar_produk[indeks]['nama'] = nama
            daftar_produk[indeks]['harga'] = harga
            daftar_produk[indeks]['stok'] = stok
            messagebox.showinfo("Sukses", "Produk berhasil diupdate!")
        
        produk_sedang_diedit = None
        tombol_tambah_edit.config(text="Tambah Produk")
        label_form.config(text="Tambah Produk Baru")
    else:
        if cari_produk(nama, daftar_produk) != -1:
            messagebox.showerror("Error", "Produk sudah ada!")
            return
        
        daftar_produk.append({'nama': nama, 'harga': harga, 'stok': stok})
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
    
    input_nama.delete(0, 'end')
    input_harga.delete(0, 'end')
    input_stok.delete(0, 'end')
    
    segarkan_tampilan_penjual()
    segarkan_tampilan_pembeli()

def muat_untuk_edit():
    global produk_sedang_diedit
    terpilih = tabel_penjual.selection()
    if not terpilih:
        messagebox.showerror("Error", "Pilih produk dulu!")
        return
    
    data = tabel_penjual.item(terpilih[0])['values']
    produk_sedang_diedit = data[0]
    
    input_nama.delete(0, 'end')
    input_nama.insert(0, data[0])
    input_harga.delete(0, 'end')
    input_harga.insert(0, data[1].replace("Rp","").replace(",",""))
    input_stok.delete(0, 'end')
    input_stok.insert(0, data[2])
    
    tombol_tambah_edit.config(text="Simpan Perubahan")
    label_form.config(text=f"Edit Produk: {data[0]}")

def hapus_produk():
    global produk_sedang_diedit
    terpilih = tabel_penjual.selection()
    if not terpilih:
        messagebox.showerror("Error", "Pilih produk dulu!")
        return
    
    nama = tabel_penjual.item(terpilih[0])['values'][0]
    
    if messagebox.askyesno("Konfirmasi", f"Hapus produk {nama}?"):
        indeks = cari_produk(nama, daftar_produk)
        if indeks != -1:
            del daftar_produk[indeks]
            messagebox.showinfo("Sukses", "Produk dihapus!")
            
            if produk_sedang_diedit == nama:
                produk_sedang_diedit = None
                input_nama.delete(0, 'end')
                input_harga.delete(0, 'end')
                input_stok.delete(0, 'end')
                tombol_tambah_edit.config(text="Tambah Produk")
                label_form.config(text="Tambah Produk Baru")
        
        segarkan_tampilan_penjual()
        segarkan_tampilan_pembeli()

def segarkan_tampilan_pembeli():
    for item in tabel_pembeli.get_children():
        tabel_pembeli.delete(item)
    
    tampilkan = []
    for produk in daftar_produk:
        if produk['stok'] > 0:
            tampilkan.append(dict(produk))
    
    if input_cari_pembeli.get():
        hasil_cari = []
        for produk in tampilkan:
            if input_cari_pembeli.get().lower() in produk['nama'].lower():
                hasil_cari.append(produk)
        tampilkan = hasil_cari
    
    urutkan_produk(tampilkan, pilihan_kriteria_pembeli.get().lower(), pilihan_urutan_pembeli.get().lower())
    
    for produk in tampilkan:
        tabel_pembeli.insert("", "end", values=(produk['nama'], f"Rp{produk['harga']:,}", produk['stok']))

def segarkan_keranjang():
    for item in tabel_keranjang.get_children():
        tabel_keranjang.delete(item)
    
    total = 0
    for item in keranjang_belanja:
        tabel_keranjang.insert("", "end", values=(
            item['nama'],
            f"Rp{item['harga']:,}",
            item['jumlah'],
            f"Rp{item['subtotal']:,}"
        ))
        total += item['subtotal']
    
    label_total.config(text=f"Total: Rp{total:,}")

def tambah_keranjang():
    terpilih = tabel_pembeli.selection()
    if not terpilih:
        messagebox.showerror("Error", "Pilih produk dulu!")
        return
    
    data = tabel_pembeli.item(terpilih[0])['values']
    nama = data[0]
    harga = int(data[1].replace("Rp","").replace(",",""))
    
    try:
        jumlah = int(input_jumlah.get())
        if jumlah <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Jumlah harus angka positif!")
        return
    
    indeks = cari_produk(nama, daftar_produk)
    if indeks == -1:
        messagebox.showerror("Error", "Produk tidak ditemukan!")
        return
    
    if jumlah > daftar_produk[indeks]['stok']:
        messagebox.showerror("Error", f"Stok tidak cukup! Tersedia: {daftar_produk[indeks]['stok']}")
        return
    
    daftar_produk[indeks]['stok'] -= jumlah
    
    ditemukan = -1
    for i, item in enumerate(keranjang_belanja):
        if item['nama'] == nama:
            ditemukan = i
            break
    
    if ditemukan != -1:
        keranjang_belanja[ditemukan]['jumlah'] += jumlah
        keranjang_belanja[ditemukan]['subtotal'] = keranjang_belanja[ditemukan]['jumlah'] * harga
    else:
        keranjang_belanja.append({
            'nama': nama,
            'harga': harga,
            'jumlah': jumlah,
            'subtotal': harga * jumlah
        })
    
    messagebox.showinfo("Sukses", f"{jumlah} {nama} ditambahkan!")
    segarkan_tampilan_pembeli()
    segarkan_keranjang()
    input_jumlah.set(1)

def hapus_dari_keranjang():
    terpilih = tabel_keranjang.selection()
    if not terpilih:
        messagebox.showerror("Error", "Pilih item dulu!")
        return
    
    data = tabel_keranjang.item(terpilih[0])['values']
    nama = data[0]
    jumlah = int(data[2])
    
    indeks = -1
    for i, item in enumerate(keranjang_belanja):
        if item['nama'] == nama:
            indeks = i
            break
    
    if indeks != -1:
        del keranjang_belanja[indeks]
        
        indeks_produk = cari_produk(nama, daftar_produk)
        if indeks_produk != -1:
            daftar_produk[indeks_produk]['stok'] += jumlah
        
        messagebox.showinfo("Sukses", f"{nama} dihapus dari keranjang!")
        segarkan_tampilan_pembeli()
        segarkan_keranjang()

def checkout():
    if not keranjang_belanja:
        messagebox.showerror("Error", "Keranjang kosong!")
        return
    
    struk = "Terima kasih telah berbelanja!\n\n"
    for item in keranjang_belanja:
        struk += f"{item['nama']} ({item['jumlah']} x Rp{item['harga']:,}) = Rp{item['subtotal']:,}\n"
    
    struk += f"\nTotal: Rp{label_total.cget('text').replace('Total: ','')}"
    messagebox.showinfo("Checkout Berhasil", struk)
    
    keranjang_belanja.clear()
    segarkan_keranjang()

def tampilkan_halaman(halaman):
    halaman_awal.pack_forget()
    halaman_penjual.pack_forget()
    halaman_pembeli.pack_forget()
    halaman.pack(fill='both', expand=True)

def ke_awal():
    global produk_sedang_diedit
    produk_sedang_diedit = None
    tombol_tambah_edit.config(text="Tambah Produk")
    label_form.config(text="Tambah Produk Baru")
    input_nama.delete(0, 'end')
    input_harga.delete(0, 'end')
    input_stok.delete(0, 'end')
    tampilkan_halaman(halaman_awal)

def ke_penjual():
    segarkan_tampilan_penjual()
    tampilkan_halaman(halaman_penjual)

def ke_pembeli():
    segarkan_tampilan_pembeli()
    segarkan_keranjang()
    tampilkan_halaman(halaman_pembeli)

# MEMBUAT TAMPILAN
app = ttk.Window(themename="minty", title="Toko MaduMart", size=(900, 700))
app.resizable(True, True)

# HALAMAN AWAL
halaman_awal = ttk.Frame(app)
label_judul = ttk.Label(halaman_awal, text="Selamat Datang di Toko MaduMart", font=("Arial", 26, "bold"))
label_judul.pack(pady=(60,30))
label_sub = ttk.Label(halaman_awal, text="Silakan Login:", font=("Arial", 16))
label_sub.pack(pady=10)

frame_tombol = ttk.Frame(halaman_awal)
frame_tombol.pack(pady=20)

tombol_penjual = ttk.Button(frame_tombol, text="Masuk sebagai Penjual", bootstyle="primary-outline", width=30, command=ke_penjual)
tombol_penjual.pack(pady=15, ipady=5)
tombol_pembeli = ttk.Button(frame_tombol, text="Masuk sebagai Pembeli", bootstyle="primary-outline", width=30, command=ke_pembeli)
tombol_pembeli.pack(pady=15, ipady=5)

# HALAMAN PENJUAL
halaman_penjual = ttk.Frame(app)

# Panel kiri
panel_kiri = ttk.Frame(halaman_penjual, padding=10)
panel_kiri.pack(side='left', fill='y', padx=10, pady=10)

label_judul_penjual = ttk.Label(panel_kiri, text="Manajemen Produk", font=("Arial", 20, "bold"))
label_judul_penjual.pack(pady=(0,15))

# Form produk
label_form = ttk.Label(panel_kiri, text="Tambah Produk Baru", font=("Arial", 12))
label_form.pack(pady=(10,5))

frame_form = ttk.Frame(panel_kiri)
frame_form.pack(pady=5)
ttk.Label(frame_form, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
input_nama = ttk.Entry(frame_form, width=30)
input_nama.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_form, text="Harga (Rp):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
input_harga = ttk.Entry(frame_form, width=30)
input_harga.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_form, text="Stok:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
input_stok = ttk.Entry(frame_form, width=30)
input_stok.grid(row=2, column=1, padx=5, pady=5)

tombol_tambah_edit = ttk.Button(frame_form, text="Tambah Produk", bootstyle="primary", command=tambah_edit_produk)
tombol_tambah_edit.grid(row=3, column=0, columnspan=2, pady=10)

ttk.Separator(panel_kiri, orient='horizontal').pack(fill='x', pady=15)

# Aksi produk
label_aksi = ttk.Label(panel_kiri, text="Aksi pada Produk Terpilih:", font=("Arial", 12))
label_aksi.pack(pady=(10,5))
frame_aksi = ttk.Frame(panel_kiri)
frame_aksi.pack(pady=5)
tombol_edit = ttk.Button(frame_aksi, text="Muat untuk Edit", bootstyle="info-outline", command=muat_untuk_edit)
tombol_edit.pack(side='left', padx=5)
tombol_hapus = ttk.Button(frame_aksi, text="Hapus Produk", bootstyle="danger-outline", command=hapus_produk)
tombol_hapus.pack(side='left', padx=5)

ttk.Separator(panel_kiri, orient='horizontal').pack(fill='x', pady=15)

# Pencarian dan pengurutan
label_cari = ttk.Label(panel_kiri, text="Pencarian & Pengurutan:", font=("Arial", 12))
label_cari.pack(pady=(10,5))
frame_cari = ttk.Frame(panel_kiri)
frame_cari.pack(pady=5, fill='x')
ttk.Label(frame_cari, text="Cari Nama:").pack(side='left', padx=(0,5))
input_cari_penjual = ttk.Entry(frame_cari, width=15)
input_cari_penjual.pack(side='left', padx=5)
tombol_cari = ttk.Button(frame_cari, text="Cari", bootstyle="secondary", command=segarkan_tampilan_penjual, width=5)
tombol_cari.pack(side='left', padx=5)

frame_urut = ttk.Frame(panel_kiri)
frame_urut.pack(pady=10, fill='x')
ttk.Label(frame_urut, text="Urutkan berdasarkan:").grid(row=0, column=0, sticky='w', padx=(0,5))
pilihan_kriteria = ttk.Combobox(frame_urut, values=["Nama", "Harga"], state="readonly", width=8)
pilihan_kriteria.set("Nama")
pilihan_kriteria.grid(row=0, column=1, padx=5)
pilihan_urutan = ttk.Combobox(frame_urut, values=["Naik", "Turun"], state="readonly", width=8)
pilihan_urutan.set("Naik")
pilihan_urutan.grid(row=0, column=2, padx=5)
tombol_urut = ttk.Button(frame_urut, text="Urutkan", bootstyle="secondary", command=segarkan_tampilan_penjual, width=7)
tombol_urut.grid(row=0, column=3, padx=5)

tombol_kembali = ttk.Button(panel_kiri, text="Kembali ke Halaman Awal", bootstyle="dark", command=ke_awal)
tombol_kembali.pack(pady=(30,10), ipady=5, fill='x')

# Panel kanan
panel_kanan = ttk.Frame(halaman_penjual, padding=10)
panel_kanan.pack(side='right', fill='both', expand=True)

label_daftar = ttk.Label(panel_kanan, text="Daftar Produk di Toko", font=("Arial", 16, "bold"))
label_daftar.pack(pady=(0,10))
tabel_penjual = ttk.Treeview(panel_kanan, columns=("Nama", "Harga", "Stok"), show="headings", bootstyle="primary")
tabel_penjual.heading("Nama", text="Nama Produk")
tabel_penjual.heading("Harga", text="Harga")
tabel_penjual.heading("Stok", text="Stok")
tabel_penjual.column("Nama", width=250, stretch=True)
tabel_penjual.column("Harga", width=120, anchor='e', stretch=False)
tabel_penjual.column("Stok", width=80, anchor='center', stretch=False)
tabel_penjual.pack(fill='both', expand=True)

# HALAMAN PEMBELI
halaman_pembeli = ttk.Frame(app)

# Panel atas
panel_atas = ttk.Frame(halaman_pembeli, padding=10)
panel_atas.pack(fill='both', expand=True, pady=(0,5))

label_judul_pembeli = ttk.Label(panel_atas, text="Pilih Produk untuk Dibeli", font=("Arial", 20, "bold"))
label_judul_pembeli.pack(pady=(0,10))

frame_cari_pembeli = ttk.Frame(panel_atas)
frame_cari_pembeli.pack(fill='x', pady=5)
ttk.Label(frame_cari_pembeli, text="Cari Nama:").pack(side='left', padx=(0,5))
input_cari_pembeli = ttk.Entry(frame_cari_pembeli, width=20)
input_cari_pembeli.pack(side='left', padx=5)
tombol_cari_pembeli = ttk.Button(frame_cari_pembeli, text="Cari", bootstyle="secondary", command=segarkan_tampilan_pembeli, width=6)
tombol_cari_pembeli.pack(side='left', padx=5)

ttk.Label(frame_cari_pembeli, text="Urutkan:").pack(side='left', padx=(15,5))
pilihan_kriteria_pembeli = ttk.Combobox(frame_cari_pembeli, values=["Nama", "Harga"], state="readonly", width=10)
pilihan_kriteria_pembeli.set("Nama")
pilihan_kriteria_pembeli.pack(side='left', padx=5)
pilihan_urutan_pembeli = ttk.Combobox(frame_cari_pembeli, values=["Naik", "Turun"], state="readonly", width=10)
pilihan_urutan_pembeli.set("Naik")
pilihan_urutan_pembeli.pack(side='left', padx=5)
tombol_urut_pembeli = ttk.Button(frame_cari_pembeli, text="Urutkan", bootstyle="secondary", command=segarkan_tampilan_pembeli, width=8)
tombol_urut_pembeli.pack(side='left', padx=5)

tabel_pembeli = ttk.Treeview(panel_atas, columns=("Nama", "Harga", "Stok"), show="headings", bootstyle="success")
tabel_pembeli.heading("Nama", text="Nama Produk")
tabel_pembeli.heading("Harga", text="Harga Satuan")
tabel_pembeli.heading("Stok", text="Stok Tersedia")
tabel_pembeli.column("Nama", width=300)
tabel_pembeli.column("Harga", width=150, anchor='e')
tabel_pembeli.column("Stok", width=100, anchor='center')
tabel_pembeli.pack(fill='both', expand=True, pady=(5,0))

# Panel bawah
panel_bawah = ttk.Frame(halaman_pembeli, padding=10)
panel_bawah.pack(fill='both', expand=True, pady=(5,0))

frame_keranjang = ttk.LabelFrame(panel_bawah, text="Keranjang Belanja Anda", bootstyle="info")
frame_keranjang.pack(fill='both', expand=True)

tabel_keranjang = ttk.Treeview(frame_keranjang, columns=("Nama", "Harga", "Jumlah", "Subtotal"), show="headings", bootstyle="info")
tabel_keranjang.heading("Nama", text="Nama Produk")
tabel_keranjang.heading("Harga", text="Harga Satuan")
tabel_keranjang.heading("Jumlah", text="Jumlah")
tabel_keranjang.heading("Subtotal", text="Subtotal")
tabel_keranjang.column("Nama", width=250)
tabel_keranjang.column("Harga", width=150, anchor='e')
tabel_keranjang.column("Jumlah", width=80, anchor='center')
tabel_keranjang.column("Subtotal", width=150, anchor='e')
tabel_keranjang.pack(fill='both', expand=True, padx=5, pady=5)

frame_kontrol = ttk.Frame(frame_keranjang)
frame_kontrol.pack(fill='x', pady=5, padx=5)
ttk.Label(frame_kontrol, text="Jumlah Beli:").pack(side='left', padx=(0,5))
input_jumlah = ttk.Spinbox(frame_kontrol, from_=1, to=100, width=5)
input_jumlah.set(1)
input_jumlah.pack(side='left', padx=5)
tombol_tambah = ttk.Button(frame_kontrol, text="Tambah ke Keranjang", bootstyle="info-outline", command=tambah_keranjang)
tombol_tambah.pack(side='left', padx=10)
tombol_hapus = ttk.Button(frame_kontrol, text="Hapus dari Keranjang", bootstyle="danger-outline", command=hapus_dari_keranjang)
tombol_hapus.pack(side='left', padx=10)

frame_total = ttk.Frame(frame_keranjang)
frame_total.pack(fill='x', pady=10, padx=5)
label_total = ttk.Label(frame_total, text="Total: Rp0", font=("Arial", 14, "bold"))
label_total.pack(side='left', expand=True)
tombol_checkout = ttk.Button(frame_total, text="Checkout", bootstyle="success", command=checkout, width=15)
tombol_checkout.pack(side='right', ipady=5)

tombol_kembali_pembeli = ttk.Button(panel_bawah, text="Kembali ke Halaman Awal", bootstyle="dark", command=ke_awal)
tombol_kembali_pembeli.pack(pady=10, ipady=5)

# DATA CONTOH
daftar_produk = [
    {'nama': "Madu Asli Premium 250ml", 'harga': 85000, 'stok': 15},
    {'nama': "Madu Royal Jelly Super 500ml", 'harga': 175000, 'stok': 8},
    {'nama': "Propolis Gold Extract 10ml", 'harga': 220000, 'stok': 12},
    {'nama': "Madu Hutan Liar 1kg", 'harga': 250000, 'stok': 5},
    {'nama': "Sarang Madu Murni 300g", 'harga': 120000, 'stok': 20}
]
urutkan_produk(daftar_produk, "nama", "naik")

# MULAI PROGRAM
tampilkan_halaman(halaman_awal)
app.mainloop()
