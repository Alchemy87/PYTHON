import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ftp_logic import MyFTP
import session_manager


class Aplicatie:
    def __init__(self, root):
        self.window = root
        self.window.title("Manager FTP - Proiect")
        self.window.geometry("600x500")
        self.client = MyFTP()

        self.frame_login = tk.Frame(self.window)
        self.frame_login.pack(pady=20)

        tk.Label(self.frame_login, text="Host:").grid(row=0, column=0)
        self.e_host = tk.Entry(self.frame_login)
        self.e_host.grid(row=0, column=1)

        tk.Label(self.frame_login, text="User:").grid(row=1, column=0)
        self.e_user = tk.Entry(self.frame_login)
        self.e_user.grid(row=1, column=1)

        tk.Label(self.frame_login, text="Pass:").grid(row=2, column=0)
        self.e_pass = tk.Entry(self.frame_login, show="*")
        self.e_pass.grid(row=2, column=1)

        tk.Button(self.frame_login, text="Conectare", command=self.do_login).grid(row=3, columnspan=2, pady=10)

        self.combo = ttk.Combobox(self.frame_login, values=list(session_manager.incarca_date().keys()))
        self.combo.grid(row=4, columnspan=2)
        self.combo.bind("<<ComboboxSelected>>", self.alege_sesiune)

    def alege_sesiune(self, ev):
        h = self.combo.get()
        date = session_manager.incarca_date()
        self.e_host.delete(0, tk.END)
        self.e_host.insert(0, h)
        self.e_user.delete(0, tk.END)
        self.e_user.insert(0, date[h]["utilizator"])

    def do_login(self):
        h, u, p = self.e_host.get(), self.e_user.get(), self.e_pass.get()
        ok, msg = self.client.connect_me(h, u, p)
        if ok:
            session_manager.salveaza_date(h, u)
            self.frame_login.destroy()
            self.interfata_manager()
        else:
            messagebox.showerror("Nop", "Nu merge: " + msg)

    def interfata_manager(self):
        self.m_frame = tk.Frame(self.window)
        self.m_frame.pack(fill="both", expand=True)

        btns = tk.Frame(self.m_frame)
        btns.pack(fill="x")
        tk.Button(btns, text="Up", command=self.go_up).pack(side="left")
        tk.Button(btns, text="Refresh", command=self.update_list).pack(side="left")
        tk.Button(btns, text="Upload", command=self.u_file).pack(side="left")
        tk.Button(btns, text="Download", command=self.d_file).pack(side="left")
        tk.Button(btns, text="Delete", command=self.del_file).pack(side="left")

        self.tree = ttk.Treeview(self.m_frame, columns=("info"), show="headings")
        self.tree.heading("info", text="Nume Fișier / Detalii")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_click)
        self.update_list()

    def update_list(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        fisiere = self.client.ia_fisiere()
        for f in fisiere:
            self.tree.insert("", "end", text=f, values=(f,))

    def on_click(self, ev):
        item = self.tree.selection()[0]
        full_line = self.tree.item(item, "text")
        nume = full_line.split()[-1]
        if self.client.intra_in_folder(nume):
            self.update_list()

    def go_up(self):
        if self.client.inapoi(): self.update_list()

    def u_file(self):
        p = filedialog.askopenfilename()
        if p:
            self.client.upload_file(p)
            self.update_list()

    def d_file(self):
        sel = self.tree.selection()
        if sel:
            nume = self.tree.item(sel[0], "text").split()[-1]
            p = filedialog.asksaveasfilename(initialfile=nume)
            if p: self.client.download_file(nume, p)

    def del_file(self):
        sel = self.tree.selection()
        if sel:
            nume = self.tree.item(sel[0], "text").split()[-1]
            if messagebox.askyesno("Confirm", "Stergem?"):
                self.client.sterge(nume)
                self.update_list()


if __name__ == "__main__":
    r = tk.Tk()
    app = Aplicatie(r)
    r.mainloop()
