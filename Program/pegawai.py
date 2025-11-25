import function
from prettytable import PrettyTable
import random
import string
from datetime import datetime

def tampilkan_data(show_all=True):
    if len(function.pegawai) == 0:
        print("Belum ada data pegawai.")
        return False

    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Jabatan", "Nomor HP", "Status", "Gaji"]

    for idp in sorted(function.pegawai.keys()):
        data = function.pegawai[idp]
        status = data.get("status", "aktif")
        g = function.gaji.get(idp, "(Belum diatur)")
        table.add_row([idp, data["nama"], data["jabatan"], data["hp"], status, g])

    print(table)
    print(f"Total Pegawai: {len(function.pegawai)}")
    return True

def tambah_data():
    try:
        idp = function.generate_id_pegawai()
        print(f"ID Pegawai otomatis: {idp}")

        nama = input("Masukkan Nama Pegawai: ").strip()
        jabatan = input("Masukkan Jabatan: ").strip()
        hp = input("Masukkan Nomor HP: ").strip()

        if not nama or not jabatan:
            print("Nama dan Jabatan tidak boleh kosong.")
            return
        if not hp.isdigit():
            print("Nomor HP harus angka.")
            return

        function.pegawai[idp] = {"nama": nama, "jabatan": jabatan, "hp": hp, "status": "aktif"}
        function.save_pegawai()

        base_username = ''.join(e for e in nama.lower() if e.isalnum())
        username = f"{base_username}{idp}"
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        i = 1
        orig = username
        while username in function.pengguna:
            username = f"{orig}{i}"
            i += 1

        function.pengguna[username] = {"password": password, "role": "pegawai", "idpegawai": idp}
        function.save_pengguna()

        print("Pegawai ditambahkan.")
        print(f"Akun otomatis → user: {username} | pass: {password}")

    except Exception as e:
        print("Kesalahan:", e)

def edit_data(id_raw):
    try:
        idp = int(id_raw)
    except:
        print("ID harus angka.")
        return

    if idp not in function.pegawai:
        print("ID tidak ditemukan.")
        return

    nama = input("Nama baru: ").strip()
    jab = input("Jabatan baru: ").strip()
    hp = input("HP baru: ").strip()

    if not hp.isdigit():
        print("HP harus angka.")
        return

    function.pegawai[idp]["nama"] = nama
    function.pegawai[idp]["jabatan"] = jab
    function.pegawai[idp]["hp"] = hp
    function.save_pegawai()

    print("Data diperbarui.")

def hapus_data(id_raw):
    try:
        idp = int(id_raw)
    except:
        print("ID harus angka.")
        return

    if idp not in function.pegawai:
        print("ID tidak ditemukan.")
        return

    confirm = input("Ketik YA untuk hapus permanen: ")
    if confirm != "YA":
        print("Dibatalkan.")
        return

    if idp in function.gaji:
        del function.gaji[idp]
        function.save_gaji()

    for u, info in list(function.pengguna.items()):
        if info.get("idpegawai") == idp:
            del function.pengguna[u]
    function.save_pengguna()

    function.cuti = [c for c in function.cuti if c["idpegawai"] != idp]
    function.save_cuti()

    function.absensi = [a for a in function.absensi if a["idpegawai"] != idp]
    function.save_absensi()

    del function.pegawai[idp]
    function.save_pegawai()

    print("Pegawai dan data terkait dihapus.")

def set_gaji():
    try:
        idp = int(input("ID Pegawai: "))
    except:
        print("Harus angka.")
        return

    if idp not in function.pegawai:
        print("ID tidak ditemukan.")
        return

    nominal = input("Nominal gaji: ")
    if not nominal.replace(".", "").isdigit():
        print("Harus angka.")
        return

    function.gaji[idp] = nominal
    function.save_gaji()
    print("Gaji disimpan.")

def lihat_gaji_sendiri(username):
    info = function.pengguna.get(username)
    if not info:
        print("Error pengguna.")
        return

    idp = info.get("idpegawai")
    if idp not in function.gaji:
        print("Gaji belum diatur.")
        return

    nama = function.pegawai.get(idp, {}).get("nama", "(tidak ada)")
    t = PrettyTable()
    t.field_names = ["ID", "Nama", "Gaji"]
    t.add_row([idp, nama, function.gaji[idp]])
    print(t)

def ajukan_cuti(idp):
    mulai = input("Mulai (YYYY-MM-DD): ")
    selesai = input("Selesai (YYYY-MM-DD): ")
    ket = input("Keterangan: ")

    function.cuti.append({
        "idpegawai": idp,
        "mulai": mulai,
        "selesai": selesai,
        "keterangan": ket
    })
    function.save_cuti()

    print("Cuti diajukan.")

def lihat_cuti_all():
    if not function.cuti:
        print("Tidak ada data cuti.")
        return

    t = PrettyTable()
    t.field_names = ["ID", "Nama", "Mulai", "Selesai", "Keterangan"]
    for c in function.cuti:
        nama = function.pegawai.get(c["idpegawai"], {}).get("nama", "(tidak)")
        t.add_row([c["idpegawai"], nama, c["mulai"], c["selesai"], c["keterangan"]])
    print(t)

def absensi(idp, jenis):
    now = datetime.now()
    function.absensi.append({
        "idpegawai": idp,
        "tanggal": now.strftime("%Y-%m-%d"),
        "waktu": now.strftime("%H:%M:%S"),
        "jenis": jenis
    })
    function.save_absensi()
    print(f"Absensi {jenis} tersimpan.")

def lihat_absensi_all():
    if not function.absensi:
        print("Belum ada absensi.")
        return

    t = PrettyTable()
    t.field_names = ["ID", "Nama", "Tanggal", "Waktu", "Jenis"]
    for a in function.absensi:
        nama = function.pegawai.get(a["idpegawai"], {}).get("nama", "(tidak)")
        t.add_row([a["idpegawai"], nama, a["tanggal"], a["waktu"], a["jenis"]])
    print(t)

def set_resign(idp):
    if idp not in function.pegawai:
        print("ID tidak ditemukan.")
        return

    function.pegawai[idp]["status"] = "resign"
    for u, info in function.pengguna.items():
        if info.get("idpegawai") == idp:
            function.pengguna[u]["idpegawai"] = None

    function.save_pegawai()
    function.save_pengguna()
    print("Pegawai di-set resign.")
