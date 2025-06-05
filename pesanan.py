
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_Formulir(object):
    def setupUi(self, Formulir):
        Formulir.setObjectName("form_pesanan")
        Formulir.resize(548, 298)
        self.verticalLayoutWidget = QtWidgets.QWidget(Formulir)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 10, 411, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayoutWidget = QtWidgets.QWidget(Formulir)
        self.formLayoutWidget.setGeometry(QtCore.QRect(130, 80, 331, 121))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.namaBarangLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.namaBarangLabel.setObjectName("namaBarangLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.namaBarangLabel)
        self.namaBarangLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.namaBarangLineEdit.setObjectName("namaBarangLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.namaBarangLineEdit)
        self.jumlahLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.jumlahLabel.setObjectName("jumlahLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.jumlahLabel)
        self.jumlahLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.jumlahLineEdit.setObjectName("jumlahLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.jumlahLineEdit)
        self.hargaLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.hargaLabel.setObjectName("hargaLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.hargaLabel)
        self.hargaLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.hargaLineEdit.setObjectName("hargaLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.hargaLineEdit)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Formulir)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(130, 210, 331, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Formulir)
        QtCore.QMetaObject.connectSlotsByName(Formulir)

        # Inisialisasi database
        self.conn = sqlite3.connect('pemesanan.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Hubungkan tombol Simpan Pesanan dengan fungsi simpan_data
        self.pushButton.clicked.connect(self.simpan_data)
        # Hubungkan tombol Batalkan dengan fungsi clear_fields
        self.pushButton_2.clicked.connect(self.clear_fields)

    def retranslateUi(self, Formulir):
        _translate = QtCore.QCoreApplication.translate
        Formulir.setWindowTitle(_translate("Formulir", "Form"))
        self.label.setText(_translate("Formulir", "Formulir Pemesanan Barang"))
        self.namaBarangLabel.setText(_translate("Formulir", "Nama Barang"))
        self.jumlahLabel.setText(_translate("Formulir", "Jumlah"))
        self.hargaLabel.setText(_translate("Formulir", "Harga"))
        self.pushButton_2.setText(_translate("Formulir", "Batalkan"))
        self.pushButton.setText(_translate("Formulir", "Simpan Pesanan"))

    def create_table(self):
        """Membuat tabel 'pesanan' jika belum ada."""
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
        """Mengambil data dari input dan menyimpannya ke database."""
        nama_barang = self.namaBarangLineEdit.text()
        jumlah = self.jumlahLineEdit.text()
        harga = self.hargaLineEdit.text()

        if not nama_barang or not jumlah or not harga:
            QMessageBox.warning(Formulir, "Peringatan", "Harap isi semua kolom.")
            return

        try:
            jumlah = int(jumlah)
            harga = float(harga)
        except ValueError:
            QMessageBox.warning(Formulir, "Peringatan", "Jumlah dan Harga harus berupa angka.")
            return

        self.cursor.execute('''
            INSERT INTO pesanan (nama_barang, jumlah, harga)
            VALUES (?, ?, ?)
        ''', (nama_barang, jumlah, harga))
        self.conn.commit()
        QMessageBox.information(Formulir, "Sukses", "Pesanan berhasil disimpan.")
        self.clear_fields()

    def clear_fields(self):
        """Membersihkan semua input fields."""
        self.namaBarangLineEdit.clear()
        self.jumlahLineEdit.clear()
        self.hargaLineEdit.clear()

if __name__ == "_main_":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Formulir = QtWidgets.QWidget()
    ui = Ui_Formulir()
    ui.setupUi(Formulir)
    Formulir.show()
    sys.exit(app.exec_())
