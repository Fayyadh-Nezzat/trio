import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# data dummy
produk_list = [
    {"nama": "Madu Asli 250ml", "harga": 75000, "stok": 10},
    {"nama": "Madu Royal Jelly", "harga": 150000, "stok": 5}
]

def halaman_utama():
    frame_penjual.pack_forget()
    frame_pembeli.pack_forget()
    frame_utama.pack(fill='both', expand=True)

def halaman_penjual():
    frame_utama.pack_forget()
    frame_pembeli.pack_forget()
    frame_penjual.pack(fill='both', expand=True)
    update_tabel_produk()

def halaman_pembeli():
    frame_utama.pack_forget()
    frame_penjual.pack_forget()
    frame_pembeli.pack(fill='both', expand=True)
    update_tabel_beli()

def tambah_produk():
    nama = entry_nama.get()
    harga = entry_harga.get()
    harga = int(harga)
    produk_list.append({"nama": nama, "harga": harga, "stok": 0})
    entry_nama.delete(0, 'end')
    entry_harga.delete(0, 'end')
    update_tabel_produk()
    

def beli_produk():
    selected = tabel_beli.selection()
    if not selected:
        messagebox.showerror("Error", "Pilih produk dulu!")
        return
    
    item = tabel_beli.item(selected[0])
    messagebox.showinfo("Berhasil", f"Berhasil membeli {item['values'][0]}")

# gui
app = ttk.Window(themename="darkly", title="MaduMart", size=(500,400))

# framesatu
frame_utama = ttk.Frame(app)
ttk.Label(frame_utama, text="Toko MaduMart", font=("Arial", 20)).pack(pady=30)
ttk.Button(frame_utama, text="Mode Penjual", command=halaman_penjual, width=20).pack(pady=10)
ttk.Button(frame_utama, text="Mode Pembeli", command=halaman_pembeli, width=20).pack(pady=10)

# framepenjual
frame_penjual = ttk.Frame(app)
ttk.Label(frame_penjual, text="Mode Penjual", font=("Arial", 16)).pack(pady=10)

# input produk
frame_input = ttk.Frame(frame_penjual)
frame_input.pack(pady=10)
ttk.Label(frame_input, text="Nama:").grid(row=0, column=0, padx=5)
entry_nama = ttk.Entry(frame_input)
entry_nama.grid(row=0, column=1, padx=5)
ttk.Label(frame_input, text="Harga:").grid(row=1, column=0, padx=5)
entry_harga = ttk.Entry(frame_input)
entry_harga.grid(row=1, column=1, padx=5)
ttk.Button(frame_input, text="Tambah", command=tambah_produk).grid(row=2, column=1, pady=5)

# tabel produk
tabel_produk = ttk.Treeview(frame_penjual, columns=("nama", "harga", "stok"), show="headings")
tabel_produk.heading("nama", text="Nama Produk")
tabel_produk.heading("harga", text="Harga")
tabel_produk.heading("stok", text="Stok")
tabel_produk.pack(fill='both', expand=True, padx=10, pady=10)

# frame pembeli
frame_pembeli = ttk.Frame(app)
ttk.Label(frame_pembeli, text="Mode Pembeli", font=("Arial", 16)).pack(pady=10)

# tabel beli
tabel_beli = ttk.Treeview(frame_pembeli, columns=("nama", "harga"), show="headings")
tabel_beli.heading("nama", text="Nama Produk")
tabel_beli.heading("harga", text="Harga")
tabel_beli.pack(fill='both', expand=True, padx=10, pady=10)
ttk.Button(frame_pembeli, text="Beli Produk", command=beli_produk).pack(pady=10)

# tombol kembali
ttk.Button(frame_penjual, text="Kembali", command=halaman_utama).pack(pady=10)
ttk.Button(frame_pembeli, text="Kembali", command=halaman_utama).pack(pady=10)

def update_tabel_produk():
    tabel_produk.delete(*tabel_produk.get_children())
    for p in produk_list:
        tabel_produk.insert("", "end", values=(p["nama"], f"Rp{p['harga']:,}", p["stok"]))

def update_tabel_beli():
    tabel_beli.delete(*tabel_beli.get_children())
    for p in produk_list:
        tabel_beli.insert("", "end", values=(p["nama"], f"Rp{p['harga']:,}"))

halaman_utama()
app.mainloop()