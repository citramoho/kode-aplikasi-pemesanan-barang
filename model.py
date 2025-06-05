import sqlite3

class Database:
    def __init__(self, db_name='pemesanan.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Membuat tabel pesanan jika belum ada."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pesanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_barang TEXT NOT NULL,
                jumlah INTEGER NOT NULL,
                harga REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_pesanan(self, nama_barang, jumlah, harga):
        """Menambahkan data pesanan ke database."""
        self.cursor.execute('''
            INSERT INTO pesanan (nama_barang, jumlah, harga)
            VALUES (?, ?, ?)
        ''', (nama_barang, jumlah, harga))
        self.conn.commit()

    def delete_pesanan(self, pesanan_id):
        """Menghapus data pesanan berdasarkan ID."""
        self.cursor.execute('DELETE FROM pesanan WHERE id = ?', (pesanan_id,))
        self.conn.commit()

    def get_all_pesanan(self):
        """Mengambil semua data pesanan."""
        self.cursor.execute('SELECT * FROM pesanan')
        return self.cursor.fetchall()

    def close(self):
        """Menutup koneksi database."""
        self.conn.close()
