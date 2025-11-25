# function.py
import csv
import os

# direk ke path folder csv
CSV_DIR = "csv"
PENGGUNA_CSV = os.path.join(CSV_DIR, "pengguna.csv")
PEGAWAI_CSV = os.path.join(CSV_DIR, "pegawai.csv")

# global variable
pengguna = {}   
pegawai = {}    
login = None    


# csv handler
def ensure_csv_dir():
    """Membuat folder CSV jika belum ada."""
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)

def load_pengguna():
    pengguna.clear()
    if not os.path.exists(PENGGUNA_CSV):
        return

    with open(PENGGUNA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            username = row[0]
            password = row[1]
            role = row[2]
            idpeg_raw = row[3] if len(row) > 3 and row[3] != "" else None
            idpegawai = int(idpeg_raw) if idpeg_raw else None

            pengguna[username] = {
                "password": password,
                "role": role,
                "idpegawai": idpegawai
            }


def save_pengguna():
    ensure_csv_dir()
    with open(PENGGUNA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for username, info in pengguna.items():
            idp = "" if info["idpegawai"] is None else info["idpegawai"]
            writer.writerow([
                username,
                info["password"],
                info["role"],
                idp
            ])


def load_pegawai():
    pegawai.clear()
    if not os.path.exists(PEGAWAI_CSV):
        return

    with open(PEGAWAI_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            try:
                idp = int(row[0])
            except:
                continue

            nama = row[1]
            jabatan = row[2]
            hp = row[3]
            gaji = row[4] if len(row) > 4 and row[4] != "" else None   

            pegawai[idp] = {
                "nama": nama,
                "jabatan": jabatan,
                "hp": hp,
                "gaji": gaji
            }


def save_pegawai():
    ensure_csv_dir()
    with open(PEGAWAI_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for idp in sorted(pegawai.keys()):
            info = pegawai[idp]
            writer.writerow([
                idp,
                info["nama"],
                info["jabatan"],
                info["hp"],
                info.get("gaji", "")   
            ])


# load & save all csv
def load_all():
    ensure_csv_dir()
    load_pengguna()
    load_pegawai()

def save_all():
    save_pengguna()
    save_pegawai()


# auto increment id pegawai
def generate_id_pegawai():
    """Generate ID baru berbasis auto-increment integer."""
    if len(pegawai) == 0:
        return 1
    return max(pegawai.keys()) + 1
