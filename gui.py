import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def halamanpenjual():
    frameawal.pack_forget()
    framekedua.pack()
    judulmart2.pack(pady=20)
    judulpenjual.pack(pady=20)
    tree.pack()

def halamanpembeli():
    frameawal.pack_forget()
    frameketiga.pack()
    judulmart3.pack(pady=20)
    judulpembeli.pack(pady=20)

#app

app = ttk.Window(themename="minty")
frameawal = ttk.Frame(app)
frameawal.pack()
labeljudul = ttk.Label(frameawal, text="Toko MaduMart", font=("Arial", 20))
labeljudul.pack(pady=20)

#buttonpebjual
buttonpenjual = ttk.Button(frameawal, text="Penjual", bootstyle="dark", width=40, command=halamanpenjual)
buttonpenjual.pack(pady=20)

#buttonpembeli
buttonpembeli = ttk.Button(frameawal, text="Pembeli", bootstyle="dark", width=40, command=halamanpembeli)
buttonpembeli.pack(pady=20)

#framekedua
framekedua = ttk.Frame(app)
judulmart2 = ttk.Label(framekedua, text="Toko MaduMart", font=("Arial", 20))

judulpenjual = ttk.Label(framekedua, text="Penjual", font=("Arial", 20))

tree = ttk.Treeview(framekedua, columns=("Nama", "Umur"), show="headings", bootstyle="dark",padding = 200)
tree.heading("Nama", text="Nama")
tree.heading("Umur", text="Umur")
tree.insert("", "end", values=("Rizal", 22))


#frameketiga
frameketiga = ttk.Frame(app)
judulmart3 = ttk.Label(frameketiga, text="Toko MaduMart", font=("Arial", 20))

judulpembeli = ttk.Label(frameketiga, text="Pembeli", font=("Arial", 20))

app.mainloop()