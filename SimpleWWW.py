__author__ = "Wojciech Kubowicz"
__email__  = "wk303204@student.polsl.pl"

import argparse
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from ttkbootstrap import Style
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys



# Tworzenie klasy aplikacji
class WebServerApp:
    def __init__(self, folder=None, port=8000, ip="127.0.0.1"):
        self.folder = folder
        self.port = port
        self.ip = ip
        self.server = None

        # Tworzenie głównego okna
        self.root = ttk.Window()
        self.root.title("Simple WWW")

        # Tworzenie stylu ttkbootstrap
        self.style = Style(theme='united')

        # Tworzenie etykiet i przycisków
        self.folder_label = ttk.Label(self.root, text="Folder:")
        self.folder_entry = ttk.Entry(self.root, state="readonly")
        self.folder_button =  ttk.Button(self.root, text="Wybierz", command=self.select_folder, bootstyle=SECONDARY)

        self.port_label = ttk.Label(self.root, text="Port:")
        self.port_entry = ttk.Entry(self.root)

        self.ip_label = ttk.Label(self.root, text="IP:")
        self.ip_entry = ttk.Entry(self.root)
        
        self.bt_frame = ttk.Frame(self.root)

        self.start_button =  ttk.Button(self.bt_frame, text="Start", command=self.start_server)
        self.stop_button =  ttk.Button(self.bt_frame, text="Stop", command=self.stop_server, state=ttk.DISABLED)

        # Układanie elementów w oknie
        self.folder_label.grid(row=0, column=0, padx=10, pady=10, sticky=ttk.E)
        self.folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky=ttk.E)
        self.folder_button.grid(row=0, column=2, padx=10, pady=10, sticky=ttk.E)

        self.port_label.grid(row=1, column=0, padx=10, pady=10, sticky=ttk.E)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)

        self.ip_label.grid(row=2, column=0, padx=10, pady=10, sticky=ttk.E)
        self.ip_entry.grid(row=2, column=1, padx=10, pady=10)

        self.bt_frame.grid(row=3, columnspan=3)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        # Ustawianie domyślnych wartości dla portu i IP
        self.port_entry.insert(ttk.END, str(port))
        self.ip_entry.insert(ttk.END, ip)

    def run(self):
        self.root.mainloop()

    def select_folder(self):
        self.folder = filedialog.askdirectory()
        self.folder_entry.configure(state="normal")
        self.folder_entry.delete(0, ttk.END)
        self.folder_entry.insert(ttk.END, self.folder)
        self.folder_entry.configure(state="readonly")


    def start_server(self):
        self.folder = self.folder_entry.get()
        self.port = int(self.port_entry.get())
        self.ip = self.ip_entry.get()

        if not self.folder:
            messagebox.showerror("Błąd", "Wybierz folder serwera.")
            return

        if self.server is not None:
            messagebox.showinfo("Informacja", "Serwer już działa.")
            return
        
        if is_port_in_use(self.ip, self.port):
            messagebox.showinfo("Błąd", "Port jest już w użyciu zmień go na inny")
            return

        self.start_button.configure(state=ttk.DISABLED)
        self.stop_button.configure(state=ttk.NORMAL)

        # Uruchamianie serwera w osobnym wątku
        self.server = subprocess.Popen(f'py -m http.server {self.port} -b {self.ip} -d {self.folder}', shell=False)

        # Otwieranie przeglądarki po uruchomieniu serwera
        url = f"http://{self.ip}:{self.port}"
        webbrowser.open(url)

    def stop_server(self):
        if self.server is not None:
            self.server.kill()

        self.start_button.configure(state=ttk.NORMAL)
        self.stop_button.configure(state=ttk.DISABLED)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Web Server App")
    parser.add_argument("--port", type=int, default=8080, help="Numer portu (domyślnie: 8080)")
    parser.add_argument("--ip", default="127.0.0.1", help="Adres IP (domyślnie: wszystkie dostępne interfejsy)")
    parser.add_argument("--folder", help="Ścieżka do folderu")
    return parser.parse_args(sys.argv[1:])

def is_port_in_use(ip: str, port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((ip, port)) == 0

def main():
    # Parsowanie argumentów wiersza poleceń
    args = parse_arguments()

    if args.folder:
        # Uruchomienie aplikacji w trybie CLI
        if is_port_in_use(args.ip, args.port):
            print(f'Port {args.port} jest w użyciu zmień port na inny!')
            return
        subprocess.Popen(f'py -m http.server {args.port} -b {args.ip} -d {args.folder}', shell=True)
    else:
        # Uruchomienie aplikacji w trybie GUI
        app = WebServerApp(args.folder, args.port, args.ip)
        app.run()

if __name__ == "__main__":
    main()
