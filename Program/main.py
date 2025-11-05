import autentikasi
from pegawai import tampilkan_data, tambah_data, edit_data, hapus_data
from prettytable import PrettyTable as PT


def buat_tabel_menu(judul, opsi):
    tabel = PT()
    tabel.field_names = [judul]
    for item in opsi:
        tabel.add_row([item])
    print(tabel)


while True:
    buat_tabel_menu(
        "PROGRAM MANAJEMEN PEGAWAI | Perusahaan Cumi Hitam Pak Kris",
        ["1. Register", "2. Login", "3. Keluar"]
    )

    menu = input("Pilih menu: ")

    if menu == "1":
        autentikasi.register()

    elif menu == "2":
        autentikasi.login_user()
        if autentikasi.login is not None:
            if autentikasi.login["role"] == "admin":
                while True:
                    buat_tabel_menu(
                        "MENU ADMIN",
                        [
                            "1. Lihat Data Pegawai",
                            "2. Tambah Pegawai",
                            "3. Edit Data Pegawai",
                            "4. Hapus Pegawai",
                            "5. Logout",
                        ]
                    )
                    pilihan = input("Pilih menu: ")

                    if pilihan == "1":
                        tampilkan_data()
                    elif pilihan == "2":
                        tambah_data()
                    elif pilihan == "3":
                        if tampilkan_data():
                            try:
                                id_edit = input("Masukkan ID Pegawai yang ingin diubah: ")
                                edit_data(id_edit)
                            except Exception as e:
                                print("Terjadi kesalahan saat memilih ID Pegawai", e)
                    elif pilihan == "4":
                        if tampilkan_data():
                            try:
                                id_hapus = input("Masukkan ID Pegawai yang ingin dihapus: ")
                                hapus_data(id_hapus)
                            except Exception as e:
                                print("Terjadi kesalahan saat memilih ID yang ingin dihapus", e)
                    elif pilihan == "5":
                        print("Logout berhasil.")
                        autentikasi.login = None
                        break
                    else:
                        print("Pilihan tidak valid.")

            elif autentikasi.login["role"] == "pengguna":
                while True:
                    buat_tabel_menu(
                        "MENU PENGGUNA",
                        ["1. Lihat Data Pegawai", "2. Logout"]
                    )
                    pilihan = input("Pilih menu: ")
                    if pilihan == "1":
                        tampilkan_data()
                    elif pilihan == "2":
                        print("Logout berhasil.")
                        autentikasi.login = None
                        break
                    else:
                        print("Pilihan tidak valid.")

    elif menu == "3":
        print("Terima kasih telah menggunakan program ini.")
        break
    else:
        print("Pilihan tidak valid.")
