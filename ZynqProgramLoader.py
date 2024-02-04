import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from ftplib import FTP
import os

class FTPUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('FTP Uploader')

        # Dropdown for selecting the process
        tk.Label(root, text="Select Modification Method:").grid(row=0, column=0, sticky=tk.W)
        self.mod_methods = {'PS': 'path_to_exe.exe', 'PL': 'path_to_script.py'}
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(root, textvariable=self.method_var, values=list(self.mod_methods.keys()), state='readonly')
        self.method_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.method_dropdown.current(0)  # Set default to first method

        # ... (rest of your __init__ code remains the same)
        # Input file selection
        tk.Label(root, text="Select Input ELF File:").grid(row=0, column=0, sticky=tk.W)
        self.input_file_path = tk.Entry(root, width=50)
        self.input_file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # FTP details entry
        tk.Label(root, text="FTP Server IP:").grid(row=1, column=0, sticky=tk.W)
        self.ftp_server_ip = tk.Entry(root, width=50)
        self.ftp_server_ip.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Username:").grid(row=2, column=0, sticky=tk.W)
        self.username = tk.Entry(root, width=50)
        self.username.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Password:").grid(row=3, column=0, sticky=tk.W)
        self.password = tk.Entry(root, show="*", width=50)
        self.password.grid(row=3, column=1, padx=5, pady=5)

        # Upload button
        tk.Button(root, text="Convert and Upload to FTP", command=self.convert_and_upload_to_ftp).grid(row=4, column=1, pady=10)


    def convert_and_upload_to_ftp(self):
        selected_method = self.method_var.get()
        input_file = self.input_file_path.get()
        ftp_server = self.ftp_server_ip.get()
        username = self.username.get()
        password = self.password.get()

        # Ensure the input file path is not empty
        if not input_file:
            messagebox.showerror("Error", "Please select a file.")
            return

        # Process the input file according to the selected method
        if selected_method == 'PS':
            # Run the .exe file
            output_bin = os.path.splitext(input_file)[0] + '.bin'
            objcopy_exe = "C:/Xilinx/Vitis/2023.2/gnu/aarch32/nt/gcc-arm-none-eabi/bin/arm-none-eabi-objcopy.exe"  # Ensure objcopy.exe is in your PATH, or specify the full path
            options = "-O binary -g"
            options_list = options.split()
            command = [objcopy_exe] + options_list + [input_file, output_bin]
            subprocess.run(command, check=True)
        elif selected_method == 'PL':
            # Run the Python script
            script_path = 'python bit_to_zynq_bin.py'
            command = ['python', script_path, input_file, output_file]
            try:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to run script: {e.stderr.decode().strip()}")
            return

        # ... (rest of your upload code remains the same)
                # Connect and upload to FTP
        try:
            ftp = FTP(ftp_server)
            ftp.login(user=username, passwd=password)
            with open(output_bin, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(output_bin)}', file)
            ftp.quit()
            messagebox.showinfo("Success", "File uploaded successfully!")
        except Exception as e:
            messagebox.showerror("FTP Error", f"Failed to upload file: {e}")

# ... (rest of your script remains the same)
def main():
    root = tk.Tk()
    app = FTPUploaderGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
