from ftplib import FTP
import os

class MyFTP:
    def __init__(self):
        self.con = FTP()

    def connect_me(self, h, u, p):
        try:
            self.con.connect(h, 21, timeout=15)
            self.con.login(u, p)
            return True, "Ok"
        except Exception as e:
            return False, str(e)

    def ia_fisiere(self):
        lista = []
        try:
            self.con.retrlines('LIST', lista.append)
            return lista
        except:
            return ["Eroare la citire"]

    def intra_in_folder(self, nume):
        try:
            self.con.cwd(nume)
            return True
        except:
            return False

    def inapoi(self):
        try:
            self.con.cwd("..")
            return True
        except:
            return False

    def download_file(self, nume_remote, cale_locala):
        f = open(cale_locala, "wb")
        self.con.retrbinary("RETR " + nume_remote, f.write)
        f.close()

    def upload_file(self, cale_locala):
        nume = os.path.basename(cale_locala)
        f = open(cale_locala, "rb")
        self.con.storbinary("STOR " + nume, f)
        f.close()

    def sterge(self, nume):
        try:
            self.con.delete(nume)
            return True
        except:
            return False
