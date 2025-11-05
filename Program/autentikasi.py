from function import pengguna, login

# prosedur register
def register():
    global pengguna
    try:
        print("=== REGISTER AKUN BARU ===")

        username = input("Masukkan username (maksimal 50 karakter): ")
        if len(username) > 50:
            print("Error: Username tidak boleh lebih dari 50 karakter.")
            return
        if username in pengguna:
            print("Error: Username sudah terdaftar.")
            return

        password = input("Masukkan password (minimal 15, maksimal 50 karakter): ")
        if len(password) < 15:
            print("Error: Password minimal 15 karakter.")
            return
        if len(password) > 50:
            print("Error: Password tidak boleh lebih dari 50 karakter.")
            return

        role = input("Masukkan role (admin/pengguna): ")
        if role not in ["admin", "pengguna"]:
            print("Error: Role tidak valid, hanya boleh 'admin' atau 'pengguna'.")
            return

        pengguna[username] = {"password": password, "role": role}
        print("Registrasi berhasil! Silakan login.")

    except Exception as e:
        print("Terjadi kesalahan saat registrasi:", e)


# prosedur login
def login_user():
    global login
    try:
        if len(pengguna) == 0:
            print("Belum ada pengguna, silakan registrasi dahulu.")
            return

        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        if username not in pengguna:
            print("Error: Username tidak ditemukan.")
            return
        if pengguna[username]["password"] != password:
            print("Error: Password salah.")
            return

        login = {"username": username, "role": pengguna[username]["role"]}
        print("Login berhasil sebagai", login["role"])

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
