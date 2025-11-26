# function.py
import csv
import os

# direk ke path folder csv
CSV_DIR = "csv"
PENGGUNA_CSV = os.path.join(CSV_DIR, "pengguna.csv")
PEGAWAI_CSV = os.path.join(CSV_DIR, "pegawai.csv")
ABSENSI_CSV = os.path.join(CSV_DIR, "absensi.csv")
RESIGN_CSV = os.path.join(CSV_DIR, "resign.csv")

# global variable
pengguna = {}   
pegawai = {}    
absensi = {}    
resign = {}     
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
            password = row[1] if len(row) > 1 else ""
            role = row[2] if len(row) > 2 else ""
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
            idp = "" if info.get("idpegawai") is None else info.get("idpegawai")
            writer.writerow([
                username,
                info.get("password",""),
                info.get("role",""),
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

            nama = row[1] if len(row) > 1 else ""
            jabatan = row[2] if len(row) > 2 else ""
            hp = row[3] if len(row) > 3 else ""
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
                info.get("nama",""),
                info.get("jabatan",""),
                info.get("hp",""),
                info.get("gaji","")
            ])

def load_absensi():
    absensi.clear()
    if not os.path.exists(ABSENSI_CSV):
        return

    with open(ABSENSI_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                idp = int(row[0])
            except:
                continue
            tanggal = row[1] if len(row) > 1 else ""
            status = row[2] if len(row) > 2 else ""
            if idp not in absensi:
                absensi[idp] = []
            absensi[idp].append({"tanggal": tanggal, "status": status})

def save_absensi():
    ensure_csv_dir()
    with open(ABSENSI_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for idp in sorted(absensi.keys()):
            for r in absensi[idp]:
                writer.writerow([idp, r.get("tanggal",""), r.get("status","")])

def load_resign():
    resign.clear()
    if not os.path.exists(RESIGN_CSV):
        return

    with open(RESIGN_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                idp = int(row[0])
            except:
                continue
            tanggal = row[1] if len(row) > 1 else ""
            alasan = row[2] if len(row) > 2 else ""
            status = row[3] if len(row) > 3 else "Pending"
            resign[idp] = {"tanggal": tanggal, "alasan": alasan, "status": status}

def save_resign():
    ensure_csv_dir()
    with open(RESIGN_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for idp in sorted(resign.keys()):
            r = resign[idp]
            writer.writerow([idp, r.get("tanggal",""), r.get("alasan",""), r.get("status","")])

def load_all():
    ensure_csv_dir()
    load_pengguna()
    load_pegawai()
    load_absensi()
    load_resign()

def save_all():
    save_pengguna()
    save_pegawai()
    save_absensi()
    save_resign()

# auto increment id pegawai
def generate_id_pegawai():
    """Generate ID baru berbasis auto-increment integer."""
    if len(pegawai) == 0:
        return 1
    return max(pegawai.keys()) + 1
