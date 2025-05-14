import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def halamanpenjual():
    frameawal.pack_forget()
    framekedua.pack(fill='both', expand=True)
    frameketiga.pack_forget()
    judulmart2.pack(pady=20)
    judulpenjual.pack(pady=10)
    frame_produk.pack(pady=10)
    tree.pack(fill='both', expand=True, padx=20, pady=10)
    frame_tombol.pack(pady=10)

def halamanpembeli():
    frameawal.pack_forget()
    framekedua.pack_forget()
    frameketiga.pack(fill='both', expand=True)
    judulmart3.pack(pady=20)
    judulpembeli.pack(pady=10)
    tree_pembeli.pack(fill='both', expand=True, padx=20, pady=10)
    frame_keranjang.pack(fill='both', expand=True, padx=20, pady=10)
    update_keranjang()

def kembali_ke_awal():
    framekedua.pack_forget()
    frameketiga.pack_forget()
    frameawal.pack(fill='both', expand=True)

def tambah_produk():
    nama = entry_nama.get()
    harga = entry_harga.get()
    stok = entry_stok.get()
    
    if not nama or not harga or not stok:
        messagebox.showerror("Error", "Semua field harus diisi!")
        return
    
    try:
        harga = int(harga)
        stok = int(stok)
        if harga <= 0 or stok <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Harga dan stok harus angka positif!")
        return
    
    tree.insert("", "end", values=(nama, f"Rp{harga:,}", stok))
    entry_nama.delete(0, 'end')
    entry_harga.delete(0, 'end')
    entry_stok.delete(0, 'end')
    messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")

def hapus_produk():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang akan dihapus!")
        return
    tree.delete(selected_item)

def tambah_ke_keranjang():
    selected_item = tree_pembeli.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang akan dibeli!")
        return
    
    try:
        jumlah = int(spinbox_jumlah.get())
        if jumlah <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka positif!")
        return
    
    item = tree_pembeli.item(selected_item)
    nama, harga, stok = item['values']
    harga_num = int(harga.replace("Rp", "").replace(",", ""))
    
    if jumlah > int(stok):
        messagebox.showerror("Error", "Stok tidak mencukupi!")
        return
    
    # Update stok di tree_pembeli
    tree_pembeli.item(selected_item, values=(nama, harga, str(int(stok) - jumlah)))
    
    # Tambahkan ke keranjang
    subtotal = harga_num * jumlah
    tree_keranjang.insert("", "end", values=(nama, harga, jumlah, f"Rp{subtotal:,}"))
    update_keranjang()

def hapus_dari_keranjang():
    selected_item = tree_keranjang.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih item yang akan dihapus!")
        return
    
    # Kembalikan stok ke tree_pembeli
    keranjang_item = tree_keranjang.item(selected_item)
    nama, harga, jumlah, _ = keranjang_item['values']
    
    for item in tree_pembeli.get_children():
        produk = tree_pembeli.item(item)
        if produk['values'][0] == nama:
            stok_sekarang = int(produk['values'][2])
            tree_pembeli.item(item, values=(nama, harga, str(stok_sekarang + int(jumlah))))
            break
    
    tree_keranjang.delete(selected_item)
    update_keranjang()

def update_keranjang():
    total = 0
    for item in tree_keranjang.get_children():
        subtotal = tree_keranjang.item(item)['values'][3]
        subtotal_num = int(subtotal.replace("Rp", "").replace(",", ""))
        total += subtotal_num
    
    label_total.config(text=f"Total: Rp{total:,}")

def checkout():
    if not tree_keranjang.get_children():
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return
    
    total = label_total.cget("text").replace("Total: ", "")
    messagebox.showinfo("Checkout Berhasil", f"Terima kasih telah berbelanja!\n\n{total}")
    
    # Kosongkan keranjang
    for item in tree_keranjang.get_children():
        tree_keranjang.delete(item)
    update_keranjang()

# Main Application
app = ttk.Window(themename="minty", title="Toko MaduMart", size=(800, 600))
app.resizable(True, True)

# Frame Awal
frameawal = ttk.Frame(app)
frameawal.pack(fill='both', expand=True)

labeljudul = ttk.Label(frameawal, text="Toko MaduMart", font=("Arial", 24, "bold"))
labeljudul.pack(pady=40)

buttonpenjual = ttk.Button(
    frameawal, 
    text="Penjual", 
    bootstyle="primary-outline", 
    width=30,
    command=halamanpenjual
)
buttonpenjual.pack(pady=20)

buttonpembeli = ttk.Button(
    frameawal, 
    text="Pembeli", 
    bootstyle="success-outline", 
    width=30,
    command=halamanpembeli
)
buttonpembeli.pack(pady=20)

# Frame Penjual
framekedua = ttk.Frame(app)

judulmart2 = ttk.Label(framekedua, text="Toko MaduMart", font=("Arial", 24, "bold"))
judulpenjual = ttk.Label(framekedua, text="Penjual", font=("Arial", 20))

# Frame untuk input produk
frame_produk = ttk.Frame(framekedua)
ttk.Label(frame_produk, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_nama = ttk.Entry(frame_produk, width=30)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_produk, text="Harga:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_harga = ttk.Entry(frame_produk, width=30)
entry_harga.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_produk, text="Stok:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_stok = ttk.Entry(frame_produk, width=30)
entry_stok.grid(row=2, column=1, padx=5, pady=5)

button_tambah = ttk.Button(
    frame_produk, 
    text="Tambah Produk", 
    bootstyle="primary", 
    command=tambah_produk
)
button_tambah.grid(row=3, column=1, pady=10, sticky='e')

# Treeview untuk daftar produk
tree = ttk.Treeview(
    framekedua, 
    columns=("Nama", "Harga", "Stok"), 
    show="headings", 
    bootstyle="primary"
)
tree.heading("Nama", text="Nama Produk")
tree.heading("Harga", text="Harga")
tree.heading("Stok", text="Stok")
tree.column("Nama", width=300)
tree.column("Harga", width=150, anchor='center')
tree.column("Stok", width=100, anchor='center')

# Frame untuk tombol aksi
frame_tombol = ttk.Frame(framekedua)
button_hapus = ttk.Button(
    frame_tombol, 
    text="Hapus Produk", 
    bootstyle="danger", 
    command=hapus_produk
)
button_hapus.pack(side='left', padx=10)

button_kembali = ttk.Button(
    frame_tombol, 
    text="Kembali", 
    bootstyle="secondary", 
    command=kembali_ke_awal
)
button_kembali.pack(side='right', padx=10)

# Frame Pembeli
frameketiga = ttk.Frame(app)

judulmart3 = ttk.Label(frameketiga, text="Toko MaduMart", font=("Arial", 24, "bold"))
judulpembeli = ttk.Label(frameketiga, text="Pembeli", font=("Arial", 20))

# Treeview untuk daftar produk pembeli
tree_pembeli = ttk.Treeview(
    frameketiga, 
    columns=("Nama", "Harga", "Stok"), 
    show="headings", 
    bootstyle="success"
)
tree_pembeli.heading("Nama", text="Nama Produk")
tree_pembeli.heading("Harga", text="Harga")
tree_pembeli.heading("Stok", text="Stok Tersedia")
tree_pembeli.column("Nama", width=250)
tree_pembeli.column("Harga", width=150, anchor='center')
tree_pembeli.column("Stok", width=150, anchor='center')

# Frame untuk keranjang belanja
frame_keranjang = ttk.LabelFrame(frameketiga, text="Keranjang Belanja", bootstyle="info")

# Treeview untuk keranjang belanja
tree_keranjang = ttk.Treeview(
    frame_keranjang, 
    columns=("Nama", "Harga", "Jumlah", "Subtotal"), 
    show="headings", 
    bootstyle="info"
)
tree_keranjang.heading("Nama", text="Nama Produk")
tree_keranjang.heading("Harga", text="Harga Satuan")
tree_keranjang.heading("Jumlah", text="Jumlah")
tree_keranjang.heading("Subtotal", text="Subtotal")
tree_keranjang.column("Nama", width=200)
tree_keranjang.column("Harga", width=150, anchor='center')
tree_keranjang.column("Jumlah", width=100, anchor='center')
tree_keranjang.column("Subtotal", width=150, anchor='center')
tree_keranjang.pack(fill='both', expand=True, padx=10, pady=10)

# Frame untuk kontrol keranjang
frame_kontrol = ttk.Frame(frame_keranjang)
frame_kontrol.pack(fill='x', pady=10)

ttk.Label(frame_kontrol, text="Jumlah:").pack(side='left', padx=5)
spinbox_jumlah = ttk.Spinbox(frame_kontrol, from_=1, to=100, width=5)
spinbox_jumlah.pack(side='left', padx=5)
spinbox_jumlah.set(1)

button_tambah_keranjang = ttk.Button(
    frame_kontrol, 
    text="Tambah ke Keranjang", 
    bootstyle="info-outline", 
    command=tambah_ke_keranjang
)
button_tambah_keranjang.pack(side='left', padx=10)

button_hapus_keranjang = ttk.Button(
    frame_kontrol, 
    text="Hapus dari Keranjang", 
    bootstyle="danger-outline", 
    command=hapus_dari_keranjang
)
button_hapus_keranjang.pack(side='left', padx=10)

# Frame untuk total dan checkout
frame_total = ttk.Frame(frame_keranjang)
frame_total.pack(fill='x', pady=10)

label_total = ttk.Label(frame_total, text="Total: Rp0", font=("Arial", 12, "bold"))
label_total.pack(side='left', padx=10, expand=True)

button_checkout = ttk.Button(
    frame_total, 
    text="Checkout", 
    bootstyle="success", 
    command=checkout
)
button_checkout.pack(side='right', padx=10)

button_kembali_pembeli = ttk.Button(
    frameketiga, 
    text="Kembali", 
    bootstyle="secondary", 
    command=kembali_ke_awal
)
button_kembali_pembeli.pack(pady=20)

# Tambahkan beberapa produk contoh
tree.insert("", "end", values=("Madu Asli 250ml", "Rp75,000", 10))
tree.insert("", "end", values=("Madu Royal Jelly 500ml", "Rp150,000", 5))
tree.insert("", "end", values=("Propolis 10ml", "Rp200,000", 8))

# Salin produk ke tree_pembeli
for item in tree.get_children():
    produk = tree.item(item)['values']
    tree_pembeli.insert("", "end", values=produk)

app.mainloop()