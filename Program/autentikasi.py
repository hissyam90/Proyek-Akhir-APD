# autentikasi.py
import function

# prosedur register
def register():
    """
    Register publik: hanya dapat membuat akun dengan role 'admin' atau 'owner'.
    Pegawai TIDAK boleh register lewat sini (admin harus membuat akun pegawai).
    """
    try:
        print("=== REGISTER AKUN BARU (owner/admin) ===")
        username = input("Masukkan username (maksimal 50 karakter): ")
        if len(username) > 50:
            print("Error: Username tidak boleh lebih dari 50 karakter.")
            return
        if username in function.pengguna:
            print("Error: Username sudah terdaftar.")
            return

        password = input("Masukkan password (minimal 15, maksimal 50 karakter): ")
        if len(password) < 15:
            print("Error: Password minimal 15 karakter.")
            return
        if len(password) > 50:
            print("Error: Password tidak boleh lebih dari 50 karakter.")
            return

        role = input("Masukkan role (owner/admin): ")
        if role not in ["owner", "admin"]:
            print("Error: Role tidak valid. Untuk registrasi publik hanya 'owner' atau 'admin'.")
            return

        # simpan
        function.pengguna[username] = {"password": password, "role": role, "idpegawai": None}
        function.save_pengguna()
        print("Registrasi berhasil! Silakan login.")

    except Exception as e:
        print("Terjadi kesalahan saat registrasi:", e)


# prosedur login
def login_user():
    global function
    try:
        if len(function.pengguna) == 0:
            print("Belum ada pengguna, silakan registrasi (owner/admin) dahulu.")
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
