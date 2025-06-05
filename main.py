import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from model import Database  # Import model database

# ---------- Login Form ----------
class LoginForm(QtWidgets.QDialog):
    def __init__(self):
        super(LoginForm, self).__init__()
        uic.loadUi("login.ui", self)

        self.loginButton = self.findChild(QtWidgets.QPushButton, "pushButton")     # Tombol Masuk
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "pushButton_2")  # Tombol Batal
        self.usernameInput = self.findChild(QtWidgets.QLineEdit, "lineEdit")       # Input Username
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")     # Input Password

        self.loginButton.clicked.connect(self.login)
        self.cancelButton.clicked.connect(self.close)

    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if username == "admin_toko" and password == "toko_sempurna":
            self.accept()  # Login sukses
        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah.")

# ---------- Formulir Pemesanan ----------
class FormulirBarang(QtWidgets.QWidget):
    def __init__(self):
        super(FormulirBarang, self).__init__()
        uic.loadUi("form_pesanan.ui", self)

        self.db = Database()  # Gunakan model.py

        self.namaBarangLineEdit = self.findChild(QtWidgets.QLineEdit, "namaBarangLineEdit")
        self.jumlahLineEdit = self.findChild(QtWidgets.QLineEdit, "jumlahLineEdit")
        self.hargaLineEdit = self.findChild(QtWidgets.QLineEdit, "hargaLineEdit")

        self.simpanButton = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.batalButton = self.findChild(QtWidgets.QPushButton, "pushButton_2")

        self.simpanButton.clicked.connect(self.simpan_data)
        self.batalButton.clicked.connect(self.clear_fields)

        # Tabel pesanan
        self.tabel = QtWidgets.QTableWidget(self)
        self.tabel.setGeometry(50, 280, 450, 150)
        self.tabel.setColumnCount(4)
        self.tabel.setHorizontalHeaderLabels(["ID", "Nama Barang", "Jumlah", "Harga"])
        self.tabel.cellDoubleClicked.connect(self.hapus_data)

        self.load_data()

    def simpan_data(self):
        nama = self.namaBarangLineEdit.text()
        jumlah = self.jumlahLineEdit.text()
        harga = self.hargaLineEdit.text()

        if not nama or not jumlah or not harga:
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi.")
            return

        try:
            jumlah = int(jumlah)
            harga = float(harga)
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Jumlah dan Harga harus berupa angka.")
            return

        self.db.insert_pesanan(nama, jumlah, harga)
        QMessageBox.information(self, "Sukses", "Pesanan berhasil disimpan.")
        self.clear_fields()
        self.load_data()

    def clear_fields(self):
        self.namaBarangLineEdit.clear()
        self.jumlahLineEdit.clear()
        self.hargaLineEdit.clear()

    def load_data(self):
        data = self.db.get_all_pesanan()
        self.tabel.setRowCount(len(data))

        for row_num, row_data in enumerate(data):
            for col_num, value in enumerate(row_data):
                self.tabel.setItem(row_num, col_num, QTableWidgetItem(str(value)))

    def hapus_data(self, row, column):
        pesanan_id = int(self.tabel.item(row, 0).text())
        confirm = QMessageBox.question(self, "Hapus Data", f"Yakin ingin menghapus pesanan ID {pesanan_id}?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            self.db.delete_pesanan(pesanan_id)
            QMessageBox.information(self, "Dihapus", f"Pesanan ID {pesanan_id} berhasil dihapus.")
            self.load_data()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

# ---------- Main ----------
def main():
    app = QtWidgets.QApplication(sys.argv)
    login = LoginForm()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = FormulirBarang()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
