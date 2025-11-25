# pegawai.py
import function
from prettytable import PrettyTable

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

        # otomatis buat akun
        username_auto = nama.lower().replace(" ", "") + str(idp)
        password_auto = "pegawai" + str(idp) + "1234567890"

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
