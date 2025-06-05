import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_Formulir(object):
    def setupUi(self, Formulir):
        Formulir.setObjectName("Formulir")
        Formulir.resize(600, 400)  # Ukuran diperbesar agar form lapang

        # Font standar
        font = QtGui.QFont()
        font.setPointSize(10)

        # Label judul
        self.verticalLayoutWidget = QtWidgets.QWidget(Formulir)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 10, 421, 71))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: blue;")
        self.verticalLayout.addWidget(self.label)

        # Form input
        self.formLayoutWidget = QtWidgets.QWidget(Formulir)
        self.formLayoutWidget.setGeometry(QtCore.QRect(100, 90, 400, 131))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.namaBarangLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.namaBarangLabel.setText("Nama Barang")
        self.namaBarangLabel.setMinimumWidth(120)
        self.namaBarangLabel.setFont(font)
        self.namaBarangLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.namaBarangLineEdit.setFont(font)

        self.jumlahLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.jumlahLabel.setText("Jumlah")
        self.jumlahLabel.setMinimumWidth(120)
        self.jumlahLabel.setFont(font)
        self.jumlahLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.jumlahLineEdit.setFont(font)

        self.hargaLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.hargaLabel.setText("Harga")
        self.hargaLabel.setMinimumWidth(120)
        self.hargaLabel.setFont(font)
        self.hargaLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.hargaLineEdit.setFont(font)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.namaBarangLabel)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.namaBarangLineEdit)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.jumlahLabel)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.jumlahLineEdit)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.hargaLabel)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.hargaLineEdit)

        # Tombol
        self.horizontalLayoutWidget = QtWidgets.QWidget(Formulir)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(100, 240, 400, 61))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setText("Batalkan")
        self.pushButton_2.setMinimumWidth(140)
        self.pushButton_2.setFont(font)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setText("Simpan Pesanan")
        self.pushButton.setMinimumWidth(140)
        self.pushButton.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Formulir)
        QtCore.QMetaObject.connectSlotsByName(Formulir)

        # Inisialisasi database
        self.conn = sqlite3.connect('pemesanan.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Tombol fungsi
        self.pushButton.clicked.connect(self.simpan_data)
        self.pushButton_2.clicked.connect(self.clear_fields)

        self.Formulir = Formulir

    def retranslateUi(self, Formulir):
        _translate = QtCore.QCoreApplication.translate
        Formulir.setWindowTitle(_translate("Formulir", "Formulir Pemesanan"))
        self.label.setText(_translate("Formulir", "Formulir Pemesanan Barang"))

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pesanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_barang TEXT,
                jumlah INTEGER,
                harga REAL
            )
        ''')
        self.conn.commit()

    def simpan_data(self):
        nama_barang = self.namaBarangLineEdit.text()
        jumlah = self.jumlahLineEdit.text()
        harga = self.hargaLineEdit.text()

        if not nama_barang or not jumlah or not harga:
            QMessageBox.warning(self.Formulir, "Peringatan", "Harap isi semua kolom.")
            return

        try:
            jumlah = int(jumlah)
            harga = float(harga)
        except ValueError:
            QMessageBox.warning(self.Formulir, "Peringatan", "Jumlah dan Harga harus berupa angka.")
            return

        self.cursor.execute('''
            INSERT INTO pesanan (nama_barang, jumlah, harga)
            VALUES (?, ?, ?)
        ''', (nama_barang, jumlah, harga))
        self.conn.commit()
        QMessageBox.information(self.Formulir, "Sukses", "Pesanan berhasil disimpan.")
        self.clear_fields()

    def clear_fields(self):
        self.namaBarangLineEdit.clear()
        self.jumlahLineEdit.clear()
        self.hargaLineEdit.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Formulir = QtWidgets.QWidget()
    ui = Ui_Formulir()
    ui.setupUi(Formulir)
    Formulir.show()
    sys.exit(app.exec_())
