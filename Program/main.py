# main.py
import autentikasi
import function
import pegawai
from prettytable import PrettyTable as PT

# load csv
function.load_all()

def buat_tabel_menu(judul, opsi):
    t = PT()
    t.field_names = [judul]
    for o in opsi:
        t.add_row([o])
    print(t)

# menu utama
while True:
    buat_tabel_menu(
        "PROGRAM MANAJEMEN PEGAWAI | Perusahaan Cumi Hitam Pak Kris",
        ["1. Register (owner/admin)", "2. Login", "3. Keluar"]
    )

    menu = input("Pilih menu: ").strip()

    if menu == "1":
        autentikasi.login_user()

        if function.login is None:
            continue

        role = function.login.get("role")

        # menu owner
        if role == "owner":
            while True:
                buat_tabel_menu(
                    "MENU OWNER",
                    [
                        "1. Lihat Data Pegawai",
                        "2. Lihat Semua Gaji",
                        "3. Tambah/Set Gaji Pegawai",
                        "4. Hapus Data Pegawai",
                        "5. Logout"
                    ]
                )
                pilihan = input("Pilih menu: ").strip()

                if pilihan == "1":
                    pegawai.tampilkan_data()

                elif pilihan == "2":
                    pegawai.lihat_semua_gaji()

                elif pilihan == "3":
                    pegawai.set_gaji()

                elif pilihan == "4":
                    if pegawai.tampilkan_data():
                        id_hapus = input("Masukkan ID Pegawai yang ingin dihapus: ").strip()
                        pegawai.hapus_data(id_hapus)

                elif pilihan == "5":
                    print("Logout berhasil.")
                    function.login = None
                    break

                else:
                    print("Pilihan tidak valid.")

        # menu admin
        elif role == "admin":
            while True:
                buat_tabel_menu(
                    "MENU ADMIN",
                    [
                        "1. Lihat Data Pegawai",
                        "2. Tambah Pegawai",
                        "3. Edit Data Pegawai",
                        "4. Buat Akun Pegawai",
                        "5. Logout"
                    ]
                )
                pilihan = input("Pilih menu: ").strip()

                if pilihan == "1":
                    pegawai.tampilkan_data()

                elif pilihan == "2":
                    pegawai.tambah_data()

                elif pilihan == "3":
                    if pegawai.tampilkan_data():
                        id_edit = input("Masukkan ID Pegawai yang ingin diubah: ").strip()
                        pegawai.edit_data(id_edit)

                elif pilihan == "4":
                    pegawai.buat_akun_pegawai()

                elif pilihan == "5":
                    print("Logout berhasil.")
                    function.login = None
                    break

                else:
                    print("Pilihan tidak valid.")

        # menu pegawai
        elif role == "pegawai":
            while True:
                buat_tabel_menu(
                    "MENU PEGAWAI",
                    ["1. Lihat Gaji Saya", "2. Logout"]
                )

                pilihan = input("Pilih menu: ").strip()

                if pilihan == "1":
                    pegawai.lihat_gaji_sendiri(function.login.get("username"))

                elif pilihan == "2":
                    print("Logout berhasil.")
                    function.login = None
                    break

                else:
                    print("Pilihan tidak valid.")

        else:
            print("Role tidak dikenali.")
            function.login = None

    elif menu == "3":
        print("Terima kasih telah menggunakan program ini.")
        break

    else:
        print("Pilihan tidak valid.")
