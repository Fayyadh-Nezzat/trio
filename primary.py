import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

DATA_PRODUK = []
KERANJANG_BELANJA = []
PRODUK_SEDANG_DIEDIT_NAMA_ASLI = None

def sequential_search_produk(nama_produk, data_list):
    found_index = -1
    i = 0
    still_searching = True
    while i < len(data_list) and still_searching:
        if data_list[i]['nama'] == nama_produk:
            found_index = i
            still_searching = False
        i += 1
    return found_index

def insertion_sort_produk(data_list, kriteria, urutan):
    n = len(data_list)
    i = 1
    while i < n:
        key_item = data_list[i]
        j = i - 1
        compare_condition_met = False
        if urutan == 'naik':
            if kriteria == 'harga':
                if j >= 0 and key_item['harga'] < data_list[j]['harga']:
                    compare_condition_met = True
            else:
                if j >= 0 and key_item['nama'] < data_list[j]['nama']:
                    compare_condition_met = True
        else:
            if kriteria == 'harga':
                if j >= 0 and key_item['harga'] > data_list[j]['harga']:
                    compare_condition_met = True
            else:
                if j >= 0 and key_item['nama'] > data_list[j]['nama']:
                    compare_condition_met = True
        
        while compare_condition_met:
            data_list[j + 1] = data_list[j]
            j -= 1
            compare_condition_met = False
            if urutan == 'naik':
                if kriteria == 'harga':
                    if j >= 0 and key_item['harga'] < data_list[j]['harga']:
                        compare_condition_met = True
                else:
                    if j >= 0 and key_item['nama'] < data_list[j]['nama']:
                        compare_condition_met = True
            else:
                if kriteria == 'harga':
                    if j >= 0 and key_item['harga'] > data_list[j]['harga']:
                        compare_condition_met = True
                else:
                    if j >= 0 and key_item['nama'] > data_list[j]['nama']:
                        compare_condition_met = True
        data_list[j + 1] = key_item
        i += 1

def refresh_penjual_treeview(search_term="", sort_criteria="nama", sort_order="naik"):
    for item in tree_penjual.get_children():
        tree_penjual.delete(item)
    display_list = list(DATA_PRODUK)
    if search_term:
        filtered_list = []
        i = 0
        while i < len(display_list):
            if search_term.lower() in display_list[i]['nama'].lower():
                filtered_list.append(display_list[i])
            i += 1
        display_list = filtered_list
    insertion_sort_produk(display_list, sort_criteria, sort_order)
    idx = 0
    while idx < len(display_list):
        produk = display_list[idx]
        tree_penjual.insert("", "end", values=(produk['nama'], f"Rp{produk['harga']:,}", produk['stok']))
        idx += 1

def muat_produk_untuk_edit():
    global PRODUK_SEDANG_DIEDIT_NAMA_ASLI
    selected_items = tree_penjual.selection()
    if not selected_items:
        messagebox.showerror("Error", "Pilih produk yang akan diedit!")
        return
    selected_item_id = selected_items[0]
    produk_values = tree_penjual.item(selected_item_id)['values']
    nama_produk_terpilih = produk_values[0]
    harga_produk_terpilih_str = produk_values[1].replace("Rp", "").replace(",", "")
    stok_produk_terpilih_str = str(produk_values[2])
    PRODUK_SEDANG_DIEDIT_NAMA_ASLI = nama_produk_terpilih
    entry_nama.delete(0, 'end')
    entry_nama.insert(0, nama_produk_terpilih)
    entry_harga.delete(0, 'end')
    entry_harga.insert(0, harga_produk_terpilih_str)
    entry_stok.delete(0, 'end')
    entry_stok.insert(0, stok_produk_terpilih_str)
    button_tambah_edit.config(text="Simpan Perubahan")
    label_form_produk.config(text=f"Edit Produk: {nama_produk_terpilih}")
    entry_nama.focus()

def aksi_tambah_atau_edit_produk():
    global PRODUK_SEDANG_DIEDIT_NAMA_ASLI
    nama = entry_nama.get()
    harga_str = entry_harga.get()
    stok_str = entry_stok.get()
    if not nama or not harga_str or not stok_str:
        messagebox.showerror("Error", "Semua field harus diisi!")
        return
    try:
        harga = int(harga_str)
        stok = int(stok_str)
        if harga <= 0 or stok < 0:
            raise ValueError("Harga atau stok tidak valid.")
    except ValueError:
        messagebox.showerror("Error", "Harga dan stok harus angka positif (stok boleh 0).")
        return
    if PRODUK_SEDANG_DIEDIT_NAMA_ASLI:
        index_produk = sequential_search_produk(PRODUK_SEDANG_DIEDIT_NAMA_ASLI, DATA_PRODUK)
        if index_produk != -1:
            if nama != PRODUK_SEDANG_DIEDIT_NAMA_ASLI:
                existing_index_new_name = sequential_search_produk(nama, DATA_PRODUK)
                if existing_index_new_name != -1:
                    messagebox.showerror("Error", f"Produk dengan nama '{nama}' sudah ada.")
                    return
            DATA_PRODUK[index_produk]['nama'] = nama
            DATA_PRODUK[index_produk]['harga'] = harga
            DATA_PRODUK[index_produk]['stok'] = stok
            messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")
        else:
            messagebox.showerror("Error", "Produk asli yang diedit tidak ditemukan.")
        PRODUK_SEDANG_DIEDIT_NAMA_ASLI = None
        button_tambah_edit.config(text="Tambah Produk")
        label_form_produk.config(text="Tambah Produk Baru")
    else:
        if sequential_search_produk(nama, DATA_PRODUK) != -1:
            messagebox.showerror("Error", f"ProduK dengan nama '{nama}' sudah ada!")
            return
        DATA_PRODUK.append({'nama': nama, 'harga': harga, 'stok': stok})
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
    entry_nama.delete(0, 'end')
    entry_harga.delete(0, 'end')
    entry_stok.delete(0, 'end')
    refresh_penjual_treeview(
        search_term_penjual.get(), 
        combo_sort_kriteria_penjual.get().lower(), 
        combo_sort_urutan_penjual.get().lower()
    )
    refresh_pembeli_treeview()

def hapus_produk_terpilih():
    global PRODUK_SEDANG_DIEDIT_NAMA_ASLI
    selected_items = tree_penjual.selection()
    if not selected_items:
        messagebox.showerror("Error", "Pilih produk yang akan dihapus!")
        return
    selected_item_id = selected_items[0]
    nama_produk_dihapus = tree_penjual.item(selected_item_id)['values'][0]
    if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus produk '{nama_produk_dihapus}'?"):
        index_to_delete = sequential_search_produk(nama_produk_dihapus, DATA_PRODUK)
        if index_to_delete != -1:
            del DATA_PRODUK[index_to_delete]
            messagebox.showinfo("Sukses", f"Produk '{nama_produk_dihapus}' berhasil dihapus.")
            if PRODUK_SEDANG_DIEDIT_NAMA_ASLI == nama_produk_dihapus:
                PRODUK_SEDANG_DIEDIT_NAMA_ASLI = None
                entry_nama.delete(0, 'end')
                entry_harga.delete(0, 'end')
                entry_stok.delete(0, 'end')
                button_tambah_edit.config(text="Tambah Produk")
                label_form_produk.config(text="Tambah Produk Baru")
        else:
            messagebox.showerror("Error", "Produk tidak ditemukan di data internal.")
        refresh_penjual_treeview(
            search_term_penjual.get(),
            combo_sort_kriteria_penjual.get().lower(),
            combo_sort_urutan_penjual.get().lower()
        )
        refresh_pembeli_treeview()

def cari_produk_penjual():
    refresh_penjual_treeview(
        search_term_penjual.get(),
        combo_sort_kriteria_penjual.get().lower(),
        combo_sort_urutan_penjual.get().lower()
    )

def urutkan_produk_penjual():
    refresh_penjual_treeview(
        search_term_penjual.get(),
        combo_sort_kriteria_penjual.get().lower(),
        combo_sort_urutan_penjual.get().lower()
    )

def refresh_pembeli_treeview(search_term="", sort_criteria="nama", sort_order="naik"):
    for item in tree_pembeli.get_children():
        tree_pembeli.delete(item)
    display_list_pembeli = []
    i = 0
    while i < len(DATA_PRODUK):
        if DATA_PRODUK[i]['stok'] > 0:
            display_list_pembeli.append(dict(DATA_PRODUK[i]))
        i += 1
    if search_term:
        filtered_list = []
        i = 0
        while i < len(display_list_pembeli):
            if search_term.lower() in display_list_pembeli[i]['nama'].lower():
                filtered_list.append(display_list_pembeli[i])
            i += 1
        display_list_pembeli = filtered_list
    insertion_sort_produk(display_list_pembeli, sort_criteria, sort_order)
    idx = 0
    while idx < len(display_list_pembeli):
        produk = display_list_pembeli[idx]
        tree_pembeli.insert("", "end", values=(produk['nama'], f"Rp{produk['harga']:,}", produk['stok']))
        idx += 1

def cari_produk_pembeli():
    refresh_pembeli_treeview(
        search_term_pembeli.get(),
        combo_sort_kriteria_pembeli.get().lower(),
        combo_sort_urutan_pembeli.get().lower()
    )

def urutkan_produk_pembeli():
    refresh_pembeli_treeview(
        search_term_pembeli.get(),
        combo_sort_kriteria_pembeli.get().lower(),
        combo_sort_urutan_pembeli.get().lower()
    )

def refresh_keranjang_treeview():
    for item in tree_keranjang.get_children():
        tree_keranjang.delete(item)
    total_harga_keranjang = 0
    i = 0
    while i < len(KERANJANG_BELANJA):
        item_keranjang = KERANJANG_BELANJA[i]
        tree_keranjang.insert("", "end", values=(
            item_keranjang['nama'], 
            f"Rp{item_keranjang['harga_satuan']:,}", 
            item_keranjang['jumlah'], 
            f"Rp{item_keranjang['subtotal']:,}"
        ))
        total_harga_keranjang += item_keranjang['subtotal']
        i += 1
    label_total.config(text=f"Total: Rp{total_harga_keranjang:,}")

def tambah_ke_keranjang():
    selected_items_pembeli = tree_pembeli.selection()
    if not selected_items_pembeli:
        messagebox.showerror("Error", "Pilih produk yang akan dibeli!")
        return
    selected_item_id = selected_items_pembeli[0]
    produk_values = tree_pembeli.item(selected_item_id)['values']
    nama_produk = produk_values[0]
    harga_str = produk_values[1].replace("Rp", "").replace(",", "")
    produk_asli_idx = sequential_search_produk(nama_produk, DATA_PRODUK)
    if produk_asli_idx == -1:
        messagebox.showerror("Error", "Produk tidak ditemukan di data utama.")
        return
    produk_asli = DATA_PRODUK[produk_asli_idx]
    harga_produk = produk_asli['harga']
    stok_tersedia = produk_asli['stok']
    try:
        jumlah_beli = int(spinbox_jumlah.get())
        if jumlah_beli <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka positif!")
        return
    if jumlah_beli > stok_tersedia:
        messagebox.showerror("Error", f"Stok tidak mencukupi! Tersedia: {stok_tersedia}")
        return
    DATA_PRODUK[produk_asli_idx]['stok'] -= jumlah_beli
    indeks_item_di_keranjang = -1
    i = 0
    searching_in_cart = True
    while i < len(KERANJANG_BELANJA) and searching_in_cart:
        if KERANJANG_BELANJA[i]['nama'] == nama_produk:
            indeks_item_di_keranjang = i
            searching_in_cart = False
        i += 1
    if indeks_item_di_keranjang != -1:
        KERANJANG_BELANJA[indeks_item_di_keranjang]['jumlah'] += jumlah_beli
        KERANJANG_BELANJA[indeks_item_di_keranjang]['subtotal'] = KERANJANG_BELANJA[indeks_item_di_keranjang]['jumlah'] * harga_produk
    else:
        KERANJANG_BELANJA.append({
            'nama': nama_produk,
            'harga_satuan': harga_produk,
            'jumlah': jumlah_beli,
            'subtotal': harga_produk * jumlah_beli
        })
    messagebox.showinfo("Sukses", f"{jumlah_beli} x {nama_produk} ditambahkan ke keranjang.")
    refresh_pembeli_treeview(
        search_term_pembeli.get(),
        combo_sort_kriteria_pembeli.get().lower(),
        combo_sort_urutan_pembeli.get().lower()
    )
    refresh_keranjang_treeview()
    spinbox_jumlah.set(1)

def hapus_dari_keranjang():
    selected_items_keranjang = tree_keranjang.selection()
    if not selected_items_keranjang:
        messagebox.showerror("Error", "Pilih item dari keranjang yang akan dihapus!")
        return
    selected_item_id = selected_items_keranjang[0]
    item_values = tree_keranjang.item(selected_item_id)['values']
    nama_produk = item_values[0]
    jumlah_dihapus_dari_keranjang = int(item_values[2])
    indeks_hapus_keranjang = -1
    i = 0
    found_in_cart = False
    while i < len(KERANJANG_BELANJA) and not found_in_cart:
        if KERANJANG_BELANJA[i]['nama'] == nama_produk:
            indeks_hapus_keranjang = i
            found_in_cart = True
        i += 1
    if indeks_hapus_keranjang != -1:
        del KERANJANG_BELANJA[indeks_hapus_keranjang]
        produk_asli_idx = sequential_search_produk(nama_produk, DATA_PRODUK)
        if produk_asli_idx != -1:
            DATA_PRODUK[produk_asli_idx]['stok'] += jumlah_dihapus_dari_keranjang
        else:
            messagebox.showwarning("Peringatan", f"Produk {nama_produk} tidak ditemukan di data utama untuk pengembalian stok.")
        messagebox.showinfo("Sukses", f"Item '{nama_produk}' dihapus dari keranjang.")
        refresh_pembeli_treeview(
            search_term_pembeli.get(),
            combo_sort_kriteria_pembeli.get().lower(),
            combo_sort_urutan_pembeli.get().lower()
        )
        refresh_keranjang_treeview()
    else:
        messagebox.showerror("Error", "Item tidak ditemukan di data keranjang internal.")

def checkout_keranjang():
    if not KERANJANG_BELANJA:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return
    total_belanja_str = label_total.cget("text").replace("Total: ", "")
    items_struk = ""
    i = 0
    while i < len(KERANJANG_BELANJA):
        item = KERANJANG_BELANJA[i]
        items_struk += f"{item['nama']} ({item['jumlah']} x Rp{item['harga_satuan']:,}) = Rp{item['subtotal']:,}\n"
        i += 1
    pesan_checkout = f"Terima kasih telah berbelanja!\n\nDetail Pembelian:\n{items_struk}\nTotal Keseluruhan: {total_belanja_str}"
    messagebox.showinfo("Checkout Berhasil", pesan_checkout)
    KERANJANG_BELANJA.clear()
    refresh_keranjang_treeview()

def tampilkan_frame(frame_target):
    frame_awal.pack_forget()
    frame_penjual_container.pack_forget()
    frame_pembeli_container.pack_forget()
    frame_target.pack(fill='both', expand=True)

def ke_halaman_awal():
    global PRODUK_SEDANG_DIEDIT_NAMA_ASLI
    PRODUK_SEDANG_DIEDIT_NAMA_ASLI = None
    button_tambah_edit.config(text="Tambah Produk")
    label_form_produk.config(text="Tambah Produk Baru")
    entry_nama.delete(0, 'end')
    entry_harga.delete(0, 'end')
    entry_stok.delete(0, 'end')
    tampilkan_frame(frame_awal)

def ke_halaman_penjual():
    refresh_penjual_treeview()
    tampilkan_frame(frame_penjual_container)

def ke_halaman_pembeli():
    refresh_pembeli_treeview()
    refresh_keranjang_treeview()
    tampilkan_frame(frame_pembeli_container)

# TAMPILAN AWAL
app = ttk.Window(themename="minty", title="Toko MaduMart", size=(900, 700))
app.resizable(True, True)

# HALAMAN AWAL
frame_awal = ttk.Frame(app)
label_judul_awal = ttk.Label(frame_awal, text="Selamat Datang di Toko MaduMart", font=("Arial", 26, "bold"))
label_judul_awal.pack(pady=(60,30))
label_sub_judul_awal = ttk.Label(frame_awal, text="Silakan pilih :", font=("Arial", 16))
label_sub_judul_awal.pack(pady=10)
frame_tombol_awal = ttk.Frame(frame_awal)
frame_tombol_awal.pack(pady=20)
button_ke_penjual = ttk.Button(frame_tombol_awal, text="Masuk sebagai Penjual", bootstyle="primary-outline", width=30, command=ke_halaman_penjual)
button_ke_penjual.pack(pady=15, ipady=5)
button_ke_pembeli = ttk.Button(frame_tombol_awal, text="Masuk sebagai Pembeli", bootstyle="primary-outline", width=30, command=ke_halaman_pembeli)
button_ke_pembeli.pack(pady=15, ipady=5)

# HALAMAN PENJUAL
frame_penjual_container = ttk.Frame(app)

# FRAME KIRI
frame_kiri_penjual = ttk.Frame(frame_penjual_container, padding=10)
frame_kiri_penjual.pack(side='left', fill='y', padx=10, pady=10)
label_judul_penjual = ttk.Label(frame_kiri_penjual, text="Manajemen Produk", font=("Arial", 20, "bold"))
label_judul_penjual.pack(pady=(0,15))

# FRAME ADD/EDIT
label_form_produk = ttk.Label(frame_kiri_penjual, text="Tambah Produk Baru", font=("Arial", 12))
label_form_produk.pack(pady=(10,5))
frame_form_produk = ttk.Frame(frame_kiri_penjual)
frame_form_produk.pack(pady=5)
ttk.Label(frame_form_produk, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_nama = ttk.Entry(frame_form_produk, width=30)
entry_nama.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_form_produk, text="Harga (Rp):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_harga = ttk.Entry(frame_form_produk, width=30)
entry_harga.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_form_produk, text="Stok:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_stok = ttk.Entry(frame_form_produk, width=30)
entry_stok.grid(row=2, column=1, padx=5, pady=5)
button_tambah_edit = ttk.Button(frame_form_produk, text="Tambah Produk", bootstyle="primary", command=aksi_tambah_atau_edit_produk)
button_tambah_edit.grid(row=3, column=0, columnspan=2, pady=10)
ttk.Separator(frame_kiri_penjual, orient='horizontal').pack(fill='x', pady=15)

# KONTROL TABEL
label_aksi_produk = ttk.Label(frame_kiri_penjual, text="Aksi pada Produk Terpilih:", font=("Arial", 12))
label_aksi_produk.pack(pady=(10,5))
frame_aksi_tree_penjual = ttk.Frame(frame_kiri_penjual)
frame_aksi_tree_penjual.pack(pady=5)
button_muat_edit = ttk.Button(frame_aksi_tree_penjual, text="Muat untuk Edit", bootstyle="info-outline", command=muat_produk_untuk_edit)
button_muat_edit.pack(side='left', padx=5)
button_hapus_produk = ttk.Button(frame_aksi_tree_penjual, text="Hapus Produk", bootstyle="danger-outline", command=hapus_produk_terpilih)
button_hapus_produk.pack(side='left', padx=5)
ttk.Separator(frame_kiri_penjual, orient='horizontal').pack(fill='x', pady=15)

# PENCARIAN DAN PENGURUTAN
label_filter_penjual = ttk.Label(frame_kiri_penjual, text="Pencarian & Pengurutan:", font=("Arial", 12))
label_filter_penjual.pack(pady=(10,5))
frame_filter_penjual = ttk.Frame(frame_kiri_penjual)
frame_filter_penjual.pack(pady=5, fill='x')
ttk.Label(frame_filter_penjual, text="Cari Nama:").pack(side='left', padx=(0,5))
search_term_penjual = ttk.Entry(frame_filter_penjual, width=15)
search_term_penjual.pack(side='left', padx=5)
button_cari_penjual = ttk.Button(frame_filter_penjual, text="Cari", bootstyle="secondary", command=cari_produk_penjual, width=5)
button_cari_penjual.pack(side='left', padx=5)
frame_sort_penjual = ttk.Frame(frame_kiri_penjual)
frame_sort_penjual.pack(pady=10, fill='x')
ttk.Label(frame_sort_penjual, text="Urutkan berdasarkan:").grid(row=0, column=0, sticky='w', padx=(0,5))
combo_sort_kriteria_penjual = ttk.Combobox(frame_sort_penjual, values=["Nama", "Harga"], state="readonly", width=8)
combo_sort_kriteria_penjual.set("Nama")
combo_sort_kriteria_penjual.grid(row=0, column=1, padx=5)
combo_sort_urutan_penjual = ttk.Combobox(frame_sort_penjual, values=["Naik", "Turun"], state="readonly", width=8)
combo_sort_urutan_penjual.set("Naik")
combo_sort_urutan_penjual.grid(row=0, column=2, padx=5)
button_urutkan_penjual = ttk.Button(frame_sort_penjual, text="Urutkan", bootstyle="secondary", command=urutkan_produk_penjual, width=7)
button_urutkan_penjual.grid(row=0, column=3, padx=5)
button_kembali_penjual = ttk.Button(frame_kiri_penjual, text="Kembali ke Halaman Awal", bootstyle="dark", command=ke_halaman_awal)
button_kembali_penjual.pack(pady=(30,10), ipady=5, fill='x')

# FRAME KANAN
frame_kanan_penjual = ttk.Frame(frame_penjual_container, padding=10)
frame_kanan_penjual.pack(side='right', fill='both', expand=True)
label_daftar_produk_penjual = ttk.Label(frame_kanan_penjual, text="Daftar Produk di Toko", font=("Arial", 16, "bold"))
label_daftar_produk_penjual.pack(pady=(0,10))
tree_penjual = ttk.Treeview(frame_kanan_penjual, columns=("Nama", "Harga", "Stok"), show="headings", bootstyle="primary")
tree_penjual.heading("Nama", text="Nama Produk")
tree_penjual.heading("Harga", text="Harga")
tree_penjual.heading("Stok", text="Stok")
tree_penjual.column("Nama", width=250, anchor='center', stretch=True)
tree_penjual.column("Harga", anchor='center', stretch=False)
tree_penjual.column("Stok", width=80, anchor='center', stretch=False)
tree_penjual.pack(fill='both', expand=True)

# HALAMAN PEMBELI
frame_pembeli_container = ttk.Frame(app)

# TABEL ATAS
panel_atas_pembeli = ttk.Frame(frame_pembeli_container, padding=10)
panel_atas_pembeli.pack(fill='both', expand=True, pady=(0,5))
label_judul_pembeli = ttk.Label(panel_atas_pembeli, text="Pilih Produk untuk Dibeli", font=("Arial", 20, "bold"))
label_judul_pembeli.pack(pady=(0,10))

# PENCARIAN DAN PENGURUTAN
frame_filter_sort_pembeli = ttk.Frame(panel_atas_pembeli)
frame_filter_sort_pembeli.pack(fill='x', pady=5)
ttk.Label(frame_filter_sort_pembeli, text="Cari Nama:").pack(side='left', padx=(0,5))
search_term_pembeli = ttk.Entry(frame_filter_sort_pembeli, width=20)
search_term_pembeli.pack(side='left', padx=5)
button_cari_pembeli = ttk.Button(frame_filter_sort_pembeli, text="Cari", bootstyle="secondary", command=cari_produk_pembeli, width=6)
button_cari_pembeli.pack(side='left', padx=5)
ttk.Label(frame_filter_sort_pembeli, text="Urutkan:").pack(side='left', padx=(15,5))
combo_sort_kriteria_pembeli = ttk.Combobox(frame_filter_sort_pembeli, values=["Nama", "Harga"], state="readonly", width=10)
combo_sort_kriteria_pembeli.set("Nama")
combo_sort_kriteria_pembeli.pack(side='left', padx=5)
combo_sort_urutan_pembeli = ttk.Combobox(frame_filter_sort_pembeli, values=["Naik", "Turun"], state="readonly", width=10)
combo_sort_urutan_pembeli.set("Naik")
combo_sort_urutan_pembeli.pack(side='left', padx=5)
button_urutkan_pembeli = ttk.Button(frame_filter_sort_pembeli, text="Urutkan", bootstyle="secondary", command=urutkan_produk_pembeli, width=8)
button_urutkan_pembeli.pack(side='left', padx=5)
tree_pembeli = ttk.Treeview(panel_atas_pembeli, columns=("Nama", "Harga", "Stok"), show="headings", bootstyle="success")
tree_pembeli.heading("Nama", text="Nama Produk")
tree_pembeli.heading("Harga", text="Harga Satuan")
tree_pembeli.heading("Stok", text="Stok Tersedia")
tree_pembeli.column("Nama", anchor= 'center')
tree_pembeli.column("Harga", anchor='center')
tree_pembeli.column("Stok", width=100, anchor='center')
tree_pembeli.pack(fill='both', expand=True, pady=(5,0))

# TABEL BAWAH
panel_bawah_pembeli = ttk.Frame(frame_pembeli_container, padding=10)
panel_bawah_pembeli.pack(fill='both', expand=True, pady=(5,0))
frame_keranjang = ttk.LabelFrame(panel_bawah_pembeli, text="Keranjang Belanja Anda", bootstyle="info")
frame_keranjang.pack(fill='both', expand=True)
tree_keranjang = ttk.Treeview(frame_keranjang, columns=("Nama", "Harga", "Jumlah", "Subtotal"), show="headings", bootstyle="info")
tree_keranjang.heading("Nama", text="Nama Produk")
tree_keranjang.heading("Harga", text="Harga Satuan")
tree_keranjang.heading("Jumlah", text="Jumlah")
tree_keranjang.heading("Subtotal", text="Subtotal")
tree_keranjang.column("Nama", anchor= 'center')
tree_keranjang.column("Harga", anchor='center')
tree_keranjang.column("Jumlah", anchor='center')
tree_keranjang.column("Subtotal", width=150, anchor='e')
tree_keranjang.pack(fill='both', expand=True, padx=5, pady=5)
frame_kontrol_keranjang = ttk.Frame(frame_keranjang)
frame_kontrol_keranjang.pack(fill='x', pady=5, padx=5)
ttk.Label(frame_kontrol_keranjang, text="Jumlah Beli:").pack(side='left', padx=(0,5))
spinbox_jumlah = ttk.Spinbox(frame_kontrol_keranjang, from_=1, to=100, width=5)
spinbox_jumlah.set(1)
spinbox_jumlah.pack(side='left', padx=5)
button_tambah_ke_keranjang = ttk.Button(frame_kontrol_keranjang, text="Tambah ke Keranjang", bootstyle="info-outline", command=tambah_ke_keranjang)
button_tambah_ke_keranjang.pack(side='left', padx=10)
button_hapus_dari_keranjang = ttk.Button(frame_kontrol_keranjang, text="Hapus dari Keranjang", bootstyle="danger-outline", command=hapus_dari_keranjang)
button_hapus_dari_keranjang.pack(side='left', padx=10)
frame_total_checkout = ttk.Frame(frame_keranjang)
frame_total_checkout.pack(fill='x', pady=10, padx=5)
label_total = ttk.Label(frame_total_checkout, text="Total: Rp0", font=("Arial", 14, "bold"))
label_total.pack(side='left', expand=True)

button_checkout = ttk.Button(frame_total_checkout, text="Checkout", bootstyle="success", command=checkout_keranjang, width=15)
button_checkout.pack(side='right', ipady=5)
button_kembali_pembeli = ttk.Button(panel_bawah_pembeli, text="Kembali ke Halaman Awal", bootstyle="dark", command=ke_halaman_awal)
button_kembali_pembeli.pack(pady=10, ipady=5)

# DATA DUMMY
def inisialisasi_data_contoh():
    global DATA_PRODUK
    DATA_PRODUK = [
        {'nama': "Madu Asli Premium 250ml", 'harga': 85000, 'stok': 15},
        {'nama': "Madu Royal Jelly Super 500ml", 'harga': 175000, 'stok': 8},
        {'nama': "Propolis Gold Extract 10ml", 'harga': 220000, 'stok': 12},
        {'nama': "Madu Hutan Liar 1kg", 'harga': 250000, 'stok': 5},
        {'nama': "Sarang Madu Murni 300g", 'harga': 120000, 'stok': 20}
    ]
    insertion_sort_produk(DATA_PRODUK, "nama", "naik")

inisialisasi_data_contoh()
tampilkan_frame(frame_awal)
app.mainloop()
