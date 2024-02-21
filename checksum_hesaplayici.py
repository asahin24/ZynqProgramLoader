import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import hashlib

class ChecksumHesaplayici(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.setup_gui()


    def setup_gui(self):
        # Dosya seçtirme butonu
        self.dosya_secme_butonu = tk.Button(self, text="Dosya seçin", command=self.checksum_hesapla)
        self.dosya_secme_butonu.grid(row=1, column=0, pady=5)

        # md5 checksum butonu
        self.md5checksum = tk.StringVar()
        self.checksum_entry = tk.Entry(self, width=35)
        self.checksum_entry.grid(row=1, column=1, pady=5)
        # self.checksum_entry.config(state='readonly')

    
    def checksum_hesapla(self):
        dosya_yolu = filedialog.askopenfilename()
        if not dosya_yolu:
            return
        
        hash_md5 = hashlib.md5()
        with open(dosya_yolu, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        # self.md5checksum = hash_md5.hexdigest()
        self.checksum_entry.config(state=tk.NORMAL)
        self.checksum_entry.delete(0, tk.END)
        self.checksum_entry.insert(0, '0x' + hash_md5.hexdigest())  # Display checksum
        self.checksum_entry.config(state="readonly")
        


    def md5(self, dosya_yolu):
        hash_md5 = hashlib.md5()
        with open(dosya_yolu, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Checksum Hesaplayıcı")
    app = ChecksumHesaplayici(root)
    app.pack(padx=10, pady=10)
    root.mainloop()