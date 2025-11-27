# pegawai.py
import function
from prettytable import PrettyTable
import datetime

# tampilkan data pegawai
def tampilkan_data():
    if len(function.pegawai) == 0:
        print("Belum ada data pegawai.")
        return False

    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Jabatan", "Nomor HP", "Gaji"]

    for idp in sorted(function.pegawai.keys()):
        data = function.pegawai[idp]
        gaji = data.get("gaji", "-") if data.get("gaji") else "-"
        table.add_row([
            idp,
            data.get("nama", ""),
            data.get("jabatan", ""),
            data.get("hp", ""),
            gaji
        ])

    print(table)
    print(f"Total Pegawai: {len(function.pegawai)}")
    return True


# tambah data pegawai
def tambah_data():
    try:
        idp = function.generate_id_pegawai()
        print(f"ID Pegawai otomatis: {idp}")

        nama = input("Masukkan Nama Pegawai: ").strip()
        jabatan = input("Masukkan Jabatan: ").strip()
        hp = input("Masukkan Nomor HP: ").strip()

        if not nama or not jabatan:
            print("Error: Nama dan Jabatan tidak boleh kosong.")
            return

        if not hp.isdigit():
            print("Error: Nomor HP harus angka.")
            return

        function.pegawai[idp] = {
            "nama": nama,
            "jabatan": jabatan,
            "hp": hp,
            "gaji": None
        }

        function.save_pegawai()

        # otomatis buat akun pegawai
        username_auto = nama.lower().replace(" ", "") + str(idp)
        password_auto = "pegawai" + str(idp) + "123456"

        function.pengguna[username_auto] = {
            "password": password_auto,
            "role": "pegawai",
            "idpegawai": idp
        }
        function.save_pengguna()

        print("Data pegawai berhasil ditambahkan.")
        print(f"Akun login otomatis dibuat:")
        print(f"  Username : {username_auto}")
        print(f"  Password : {password_auto}")

    except Exception as e:
        print("Terjadi kesalahan saat menambah data:", e)


# edit data pegawai
def edit_data(id_edit_raw):
    try:
        id_edit = int(id_edit_raw)
    except:
        print("Error: ID harus berupa angka.")
        return

    if id_edit not in function.pegawai:
        print("Error: ID pegawai tidak ditemukan.")
        return

    nama_baru = input("Masukkan Nama baru: ").strip()
    jabatan_baru = input("Masukkan Jabatan baru: ").strip()
    hp_baru = input("Masukkan Nomor HP baru: ").strip()

    if not nama_baru or not jabatan_baru:
        print("Error: Nama dan Jabatan tidak boleh kosong.")
        return

    if not hp_baru.isdigit():
        print("Error: Nomor HP harus angka.")
        return

    function.pegawai[id_edit]["nama"] = nama_baru
    function.pegawai[id_edit]["jabatan"] = jabatan_baru
    function.pegawai[id_edit]["hp"] = hp_baru

    function.save_pegawai()
    print("Data berhasil diperbarui.")


#  ngehapus data pegawai
def hapus_data(id_hapus_raw):
    try:
        id_hapus = int(id_hapus_raw)
    except:
        print("Error: ID harus berupa angka.")
        return

    if id_hapus not in function.pegawai:
        print("Error: ID pegawai tidak ditemukan.")
        return

    # hapus akun pegawai yang terhubung ke idpegawai
    hapus_user_list = []
    for username, info in function.pengguna.items():
        if info.get("idpegawai") == id_hapus:
            hapus_user_list.append(username)

    for u in hapus_user_list:
        del function.pengguna[u]

    function.save_pengguna()

    # hapus absensi terkait
    if id_hapus in function.absensi:
        del function.absensi[id_hapus]
        function.save_absensi()

    # hapus resign terkait
    if id_hapus in function.resign:
        del function.resign[id_hapus]
        function.save_resign()

    # hapus pegawai
    del function.pegawai[id_hapus]
    function.save_pegawai()

    print("Data pegawai berhasil dihapus.")


# admin ngebuat akun pegawai
def buat_akun_pegawai():
    try:
        if len(function.pegawai) == 0:
            print("Belum ada data pegawai. Tambahkan pegawai terlebih dahulu.")
            return

        # tampilkan tabel pegawai dulu
        t = PrettyTable()
        t.field_names = ["ID", "Nama", "Jabatan", "HP"]

        for idp in sorted(function.pegawai.keys()):
            d = function.pegawai[idp]
            t.add_row([idp, d["nama"], d["jabatan"], d["hp"]])

        print(t)

        # ambil id yang valid
        while True:
            idp_raw = input("Masukkan ID Pegawai yang sudah terdaftar (atau ketik 'batal'): ").strip()

            if idp_raw.lower() == "batal":
                print("Dibatalkan.")
                return

            try:
                idp = int(idp_raw)
            except:
                print("ID tidak valid, harus angka.")
                continue

            if idp not in function.pegawai:
                print("ID tidak ditemukan. Periksa tabel di atas.")
                continue

            break  

        # username akun pegawai
        username = input("Masukkan username untuk pegawai: ").strip()
        if username in function.pengguna:
            print("Error: Username sudah digunakan.")
            return

        password = input("Masukkan password (minimal 15 karakter): ").strip()
        if len(password) < 15:
            print("Error: Password minimal 15 karakter.")
            return

        # simpan akun
        function.pengguna[username] = {
            "password": password,
            "role": "pegawai",
            "idpegawai": idp
        }

        function.save_pengguna()
        print(f"Akun pegawai '{username}' berhasil dibuat dan terhubung ke ID {idp}.")

    except Exception as e:
        print("Terjadi kesalahan saat membuat akun pegawai:", e)


# owner liat semua gaji pegawai
def lihat_semua_gaji():

    if len(function.pegawai) == 0:
        print("Belum ada data pegawai.")
        return

    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Gaji"]

    for idp in sorted(function.pegawai.keys()):
        d = function.pegawai[idp]
        gaji = d.get("gaji", "-")
        t.add_row([idp, d["nama"], gaji])

    print(t)


# owner ngegaji pegawai
def set_gaji():

    # tampilkan daftar pegawai 
    if len(function.pegawai) == 0:
        print("Belum ada data pegawai.")
        return

    t = PrettyTable()
    t.field_names = ["ID", "Nama", "Jabatan", "Nomor HP", "Gaji"]

    for idp in sorted(function.pegawai.keys()):
        d = function.pegawai[idp]
        gaji_val = d.get("gaji", "-") if d.get("gaji") else "-"
        t.add_row([idp, d["nama"], d["jabatan"], d["hp"], gaji_val])

    print(t)

    try:
        idp_raw = input("Masukkan ID Pegawai: ").strip()
        idp = int(idp_raw)
    except:
        print("Error: ID harus berupa angka.")
        return

    if idp not in function.pegawai:
        print("Error: ID pegawai tidak ditemukan.")
        return

    nominal = input("Masukkan nominal gaji: ").strip()
    if not nominal.replace(".", "", 1).isdigit():
        print("Error: Gaji harus angka.")
        return

    # simpan gaji ke pegawai.csv
    function.pegawai[idp]["gaji"] = nominal
    function.save_pegawai()

    print("Gaji berhasil disimpan.")


#  pegawai liat gaji sendiri
def lihat_gaji_sendiri(username):
    info = function.pengguna.get(username)

    if not info:
        print("Error: Pegawai tidak ditemukan.")
        return

    idp = info.get("idpegawai")

    d = function.pegawai.get(idp)

    if not d or d.get("gaji") is None:
        print("Gaji belum diatur.")
        return

    nama = d.get("nama", "(Tidak Terdaftar)")

    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Gaji"]
    t.add_row([idp, nama, d["gaji"]])

    print(t)


# absensi pegawai

def absen(username):
    info = function.pengguna.get(username)
    if not info:
        print("Error: Pengguna tidak ditemukan.")
        return

    idp = info.get("idpegawai")
    if idp not in function.pegawai:
        print("Pegawai tidak ditemukan.")
        return

    hari_ini = datetime.date.today().strftime("%Y-%m-%d")

    # cek apakah sudah absen hari ini
    user_absen = function.absensi.get(idp, [])
    for r in user_absen:
        if r.get("tanggal") == hari_ini:
            print("Anda sudah melakukan absensi hari ini.")
            return

    print("Pilih status absensi:")
    print("1. Hadir")
    print("2. Izin")
    print("3. Sakit")

    pilih = input("Pilih: ").strip()
    status_map = {"1": "Hadir", "2": "Izin", "3": "Sakit"}
    if pilih not in status_map:
        print("Pilihan tidak valid.")
        return

    status = status_map[pilih]

    if idp not in function.absensi:
        function.absensi[idp] = []

    function.absensi[idp].append({"tanggal": hari_ini, "status": status})
    function.save_absensi()
    print("Absensi berhasil disimpan.")


def lihat_absensi_sendiri(username):
    info = function.pengguna.get(username)
    if not info:
        print("Error: Pengguna tidak ditemukan.")
        return

    idp = info.get("idpegawai")
    data = function.absensi.get(idp, [])

    if not data:
        print("Belum ada data absensi.")
        return

    t = PrettyTable()
    t.field_names = ["Tanggal", "Status"]

    for r in data:
        t.add_row([r.get("tanggal",""), r.get("status","")])

    print(t)


def lihat_absensi_semua():
    if len(function.absensi) == 0:
        print("Belum ada data absensi.")
        return

    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Tanggal", "Status"]

    for idp in sorted(function.absensi.keys()):
        nama = function.pegawai.get(idp, {}).get("nama", "(Tidak Terdaftar)")
        for r in function.absensi.get(idp, []):
            t.add_row([idp, nama, r.get("tanggal",""), r.get("status","")])

    print(t)

# fitur resign
def ajukan_resign(username):
    info = function.pengguna.get(username)
    if not info:
        print("Error: Pengguna tidak ditemukan.")
        return

    idp = info.get("idpegawai")

    # jika sudah pernah ajukan
    if idp in function.resign:
        print("Anda sudah pernah mengajukan resign.")
        print("Status saat ini:", function.resign[idp]["status"])
        return

    alasan = input("Masukkan alasan resign: ").strip()
    if not alasan:
        print("Alasan tidak boleh kosong.")
        return

    tanggal = datetime.date.today().strftime("%Y-%m-%d")

    function.resign[idp] = {
        "tanggal": tanggal,
        "alasan": alasan,
        "status": "Pending"
    }
    function.save_resign()

    print("Pengajuan resign berhasil dikirim.")


def lihat_resign_sendiri(username):
    info = function.pengguna.get(username)
    if not info:
        print("Error: Pengguna tidak ditemukan.")
        return

    idp = info.get("idpegawai")

    if idp not in function.resign:
        print("Anda belum mengajukan resign.")
        return

    r = function.resign[idp]

    t = PrettyTable()
    t.field_names = ["Tanggal", "Alasan", "Status"]
    t.add_row([r["tanggal"], r["alasan"], r["status"]])
    print(t)


def menu_resign_owner():
    if len(function.resign) == 0:
        print("Belum ada pengajuan resign.")
        return

    # tampilkan semua resign
    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Tanggal", "Alasan", "Status"]

    for idp, r in sorted(function.resign.items()):
        nama = function.pegawai.get(idp, {}).get("nama", "(Tidak Terdaftar)")
        t.add_row([idp, nama, r["tanggal"], r["alasan"], r["status"]])

    print(t)

    # tanya apakah ingin update status
    pilihan = input("Apakah ingin mengubah status pengajuan resign? (y/n): ").strip().lower()

    if pilihan != "y":
        print("Kembali ke menu owner...")
        return

    # proses ubah status
    try:
        idp_raw = input("Masukkan ID pegawai: ").strip()
        idp = int(idp_raw)
    except:
        print("ID tidak valid.")
        return

    if idp not in function.resign:
        print("Pegawai ini tidak memiliki pengajuan resign.")
        return

    print("Pilih status baru:")
    print("1. Pending")
    print("2. Diterima")
    print("3. Ditolak")

    pilih = input("Pilih: ").strip()
    status_map = {
        "1": "Pending",
        "2": "Diterima",
        "3": "Ditolak"
    }

    if pilih not in status_map:
        print("Pilihan tidak valid.")
        return

    function.resign[idp]["status"] = status_map[pilih]
    function.save_resign()

    print("Status pengajuan resign berhasil diperbarui.")
