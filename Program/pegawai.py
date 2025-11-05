from function import pegawai, hitung_pegawai
from prettytable import PrettyTable

# fungsi tanpa parameter
def tampilkan_data():
    global pegawai
    try:
        if len(pegawai) == 0:
            print("Belum ada data pegawai.")
            return False

        print("=== DATA PEGAWAI ===")
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Jabatan", "Nomor HP"]
        for idp, data in pegawai.items():
            table.add_row([idp, data['nama'], data['jabatan'], data['hp']])
        print(table)
        print(f"Total pegawai: {hitung_pegawai(list(pegawai.keys()))}")
        print("================================")
        return True

    except Exception as e:
        print("Terjadi kesalahan saat menampilkan data:", e)
        return False


# fungsi tanpa parameter
def tambah_data():
    global pegawai
    try:
        idp = input("Masukkan ID Pegawai (hanya angka): ")
        if idp in pegawai:
            print("Error: ID pegawai sudah terdaftar.")
            return
        if not idp.isdigit():
            print("Error: ID harus berupa angka.")
            return

        nama = input("Masukkan Nama Pegawai: ")       
        jabatan = input("Masukkan Jabatan: ")
        if jabatan == "" or nama == "":
            print("Error: Jabatan atau Nama tidak boleh kosong.")
            return
        hp = input("Masukkan Nomor HP: ")
        if not hp.isdigit():
            print("Error: Nomor HP harus berupa angka.")
            return

        pegawai[idp] = {"nama": nama, "jabatan": jabatan, "hp": hp}
        print("Data pegawai berhasil ditambahkan.")

    except Exception as e:
        print("Terjadi kesalahan saat menambah data:", e)


# fungsi dengan parameter
def edit_data(id_edit):
    global pegawai
    try:
        if not id_edit.isdigit():
            print("Error: ID harus berupa angka.")
            return
        if id_edit not in pegawai:
            print("Error: ID pegawai tidak ditemukan.")
            return

        nama_baru = input("Masukkan Nama baru: ")
        jabatan_baru = input("Masukkan Jabatan baru: ")
        if jabatan_baru == "" or nama_baru == "":
            print("Error: Jabatan atau Nama tidak boleh kosong.")
            return
        hp_baru = input("Masukkan Nomor HP baru: ")
        if not hp_baru.isdigit():
            print("Error: Nomor HP harus berupa angka.")
            return

        pegawai[id_edit]["nama"] = nama_baru
        pegawai[id_edit]["jabatan"] = jabatan_baru
        pegawai[id_edit]["hp"] = hp_baru
        print("Data berhasil diperbarui.")

    except Exception as e:
        print("Terjadi kesalahan saat mengedit data:", e)


# fungsi dengan parameter
def hapus_data(id_hapus):
    global pegawai
    try:
        if not id_hapus.isdigit():
            print("Error: ID harus berupa angka.")
            return
        if id_hapus not in pegawai:
            print("Error: ID pegawai tidak ditemukan.")
            return

        del pegawai[id_hapus]
        print("Data pegawai berhasil dihapus.")

    except Exception as e:
        print("Terjadi kesalahan saat menghapus data:", e)
