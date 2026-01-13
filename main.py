import tkinter as tk
from tkinter import messagebox, ttk
from ftplib import FTP
import session_manager



class FTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI FTP Manager - Phase A")
        self.root.geometry("400x400")

        # UI Login
        tk.Label(root, text="FTP Host:").pack(pady=5)
        self.host_entry = ttk.Entry(root)
        self.host_entry.pack(pady=5)

        tk.Label(root, text="Username:").pack(pady=5)
        self.user_entry = ttk.Entry(root)
        self.user_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.pass_entry = ttk.Entry(root, show="*")
        self.pass_entry.pack(pady=5)

        self.conn_btn = ttk.Button(root, text="Connect & Save", command=self.handle_login)
        self.conn_btn.pack(pady=20)

        tk.Label(root, text="Saved Sessions:").pack(pady=5)
        self.session_box = ttk.Combobox(root, values=list(session_manager.load_sessions().keys()))
        self.session_box.pack(pady=5)
        self.session_box.bind("<<ComboboxSelected>>", self.load_selected_session)

    def load_selected_session(self, event):
        host = self.session_box.get()
        sessions = session_manager.load_sessions()
        if host in sessions:
            self.host_entry.delete(0, tk.END)
            self.host_entry.insert(0, host)
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, sessions[host]["user"])

    def handle_login(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        try:
            ftp = FTP(host)
            ftp.login(user, password)
            session_manager.save_session(host, user)
            messagebox.showinfo("Succes", "Conectat cu succes!")
            ftp.quit()
        except Exception as e:
            messagebox.showerror("Eroare", f"Conexiune eșuată: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FTPApp(root)
    root.mainloop()
