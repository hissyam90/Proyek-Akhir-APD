# autentikasi.py
import function

# prosedur login
def login_user():
    global function
    try:
        if len(function.pengguna) == 0:
            print("Belum ada pengguna, silakan registrasi dahulu.")
            return

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        if username not in function.pengguna:
            print("Error: Username tidak ditemukan.")
            return
        if function.pengguna[username]["password"] != password:
            print("Error: Password salah.")
            return

        # set global login reference di module function
        info = function.pengguna[username]
        # include idpegawai apabila ada
        function.login = {"username": username, "role": info.get("role"), "idpegawai": info.get("idpegawai")}
        print("Login berhasil sebagai", function.login["role"])

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
