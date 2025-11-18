# pegawai.py
import function
from prettytable import PrettyTable

# tampilkan data pegawai
def tampilkan_data():
    if len(function.pegawai) == 0:
        print("Belum ada data pegawai.")
        return False

    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Jabatan", "Nomor HP"]

    for idp in sorted(function.pegawai.keys()):
        data = function.pegawai[idp]
        table.add_row([
            idp,
            data.get("nama", ""),
            data.get("jabatan", ""),
            data.get("hp", "")
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
            "hp": hp
        }

        function.save_pegawai()
        print("Data pegawai berhasil ditambahkan.")

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

    # hapus gaji kalau ada
    if id_hapus in function.gaji:
        del function.gaji[id_hapus]
        function.save_gaji()

    # hapus idpegawai di pengguna
    for username, info in function.pengguna.items():
        if info.get("idpegawai") == id_hapus:
            function.pengguna[username]["idpegawai"] = None
    function.save_pengguna()

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

            break  # id valid

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
    if len(function.gaji) == 0:
        print("Belum ada data gaji.")
        return

    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Gaji"]

    for idp in sorted(function.gaji.keys()):
        nama = function.pegawai.get(idp, {}).get("nama", "(Tidak Terdaftar)")
        t.add_row([idp, nama, function.gaji[idp]])

    print(t)


# owner ngegaji pegawai
def set_gaji():
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

    function.gaji[idp] = nominal
    function.save_gaji()

    print("Gaji berhasil disimpan.")


#  pegawai liat gaji sendiri
def lihat_gaji_sendiri(username):
    info = function.pengguna.get(username)

    if not info:
        print("Error: Pegawai tidak ditemukan.")
        return

    idp = info.get("idpegawai")

    if idp not in function.gaji:
        print("Gaji belum diatur.")
        return

    nama = function.pegawai.get(idp, {}).get("nama", "(Tidak Terdaftar)")

    t = PrettyTable()
    t.field_names = ["ID Pegawai", "Nama", "Gaji"]
    t.add_row([idp, nama, function.gaji[idp]])

    print(t)
