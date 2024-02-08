import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from ftplib import FTP
import os

class FTPUploaderGUI:
    def __init__(self, master, on_ip_click=None,):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.ftp_server_ip = None  # Initialize the FTP server IP attribute
        self.setup_gui()

        
    def setup_gui(self):
        # Dropdown for selecting the process
        tk.Label(self.frame, text="Dosya Türü:").grid(row=0, column=0, sticky=tk.W)
        self.mod_methods = {'PS': 'elf dosya yolu', 'PL': 'bit dosya yolu'}
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(self.frame, textvariable=self.method_var, values=list(self.mod_methods.keys()), state='readonly')
        self.method_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.method_dropdown.current(0)  # Set default to first method

        # Input file selection
        tk.Label(self.frame, text="Dosyayı seçiniz:").grid(row=1, column=0, sticky=tk.W)
        self.input_file_path = tk.Entry(self.frame, width=50)
        self.input_file_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Araştır", command=self.browse_file).grid(row=1, column=2, padx=5, pady=5)

        # FTP details entry
        #tk.Label(self.frame, text="FTP Server IP:").grid(row=2, column=0, sticky=tk.W)
        #self.ftp_server_ip = tk.Entry(self.frame, width=50)
        #self.ftp_server_ip.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Kullanıcı Adı:").grid(row=3, column=0, sticky=tk.W)
        self.username = tk.Entry(self.frame, width=50)
        self.username.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Şifre:").grid(row=4, column=0, sticky=tk.W)
        self.password = tk.Entry(self.frame, show="*", width=50)
        self.password.grid(row=4, column=1, padx=5, pady=5)

        # Upload button
        tk.Button(self.frame, text="Dosyayı Çevir ve Gönder", command=self.cevir_ve_gonder).grid(row=5, column=1, pady=10)


    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=(("ELF dosyaları", "*.elf"), ("Bit dosyaları", "*.*")))
        self.input_file_path.delete(0, tk.END)
        self.input_file_path.insert(0, filename)


    def cevir_ve_gonder(self):
        selected_method = self.method_var.get()
        input_file = self.input_file_path.get()
        # Use the stored ftp_server_ip attribute
        ftp_server = self.ftp_server_ip
        username = self.username.get()
        password = self.password.get()

        # Your existing file processing and FTP upload logic
        if not ftp_server:
            messagebox.showerror("Hata", "FTP sunucusu IP adresi belirtilmemiş.")
            return

        # Ensure the input file path is not empty
        if not input_file:
            messagebox.showerror("Hata", "Lütfen bir dosya seçin.")
            return
        
        output_file = os.path.splitext(input_file)[0] + '.bin'
        # Process the input file according to the selected method
        if selected_method == 'PS':
            # Run the .exe file   
            objcopy_exe = "C:/Xilinx/Vitis/2023.2/gnu/aarch32/nt/gcc-arm-none-eabi/bin/arm-none-eabi-objcopy.exe"  # Ensure objcopy.exe is in your PATH, or specify the full path
            options = "-O binary -g"
            options_list = options.split()
            command = [objcopy_exe] + options_list + [input_file, output_file]
            subprocess.run(command, check=True)
        elif selected_method == 'PL':
            # Run the Python script
            script_path = 'harici/ZynqProgramLoader/bit_to_zynq_bin.py'
            command = ['python', script_path, input_file, output_file]
            try:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to run script: {e.stderr.decode().strip()}")
                return

                # Connect and upload to FTP
        try:
            ftp = FTP(ftp_server)
            ftp.login(user=username, passwd=password)
            with open(output_file, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(output_file)}', file)
            ftp.quit()
            messagebox.showinfo("Success", "Dosya Başarılı Şekilde Yüklendi!")
        except Exception as e:
            messagebox.showerror("FTP Error", f"Failed to upload file: {e}")

        
    def update_ftp_server_ip(self, ip_address):
        #Update the FTP server IP address in the GUI.
        self.ftp_server_ip = ip_address
        #self.ftp_server_ip.delete(0, tk.END)  # Remove the current content
        #self.ftp_server_ip.insert(0, ip_address)  # Insert the new IP address
