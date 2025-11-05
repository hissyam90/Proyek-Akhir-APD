# variabel global
pengguna = {}
pegawai = {}
login = None

# fungsi rekursif ngitung jumlah data pegawai    
def hitung_pegawai(keys):
    if not keys:
        return 0
    else:
        return 1 + hitung_pegawai(keys[1:])