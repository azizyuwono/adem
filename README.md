# adem

> Biar MacBook nggak kepanasan sendiri.

Bekerja di mesin yang sama setiap hari itu Capek, apalagi kalau mesin itu sudah berumur dan cenderung gampang panas.

Repo ini adalah teman yang jaga dari jauh. Ia memonitor kondisi CPU, RAM, dan suhu sistem. Kalau ada tanda-tanda sistem mulai kepanasan atau beban kerja terlalu berat, ia ambil langkah sederhana untuk meredamnya — purge memory, tekan proses yang lari liar, atau catat saja apa yang sedang terjadi.

Ia tidak sempurna. Tapi ia selalu ada.

## Apa Yang Dipantau

- **CPU Usage** — apakah sedang bekerja terlalu keras.
- **Thermal State** — apakah suhu sudah masuk zona bahaya.
- **Memory Pressure** — apakah RAM hampir penuh.

## Respons Otomatis

Kalau sistem terlihat tidak sehat, `adem` mengambil satu atau beberapa langkah kecil:

- **Cool Down** — kosongkan cache, hentikan proses yang tidak kritis.
- **Log** — catat semua yang terjadi biar bisa dibaca nanti.

## Struktur Kode

```
src/
├── watcher.py   # Ngambil data dari sistem
├── healer.py    # Ambil keputusan dan bertindak
└── main.py      # Jalankan semuanya

tests/
└── test_core.py # Cek apakah bagian-bagiannya masih jalan

.github/workflows/
└── daily.yml    # Berjalan otomatis setiap hari
```

## Jalanin di Komputer Sendiri

```bash
git clone git@github.com:azizyuwono/adem.git
cd adem
pip install -r requirements.txt
python -m src.main
```

---

_dikelola oleh [Moli](https://t.me/davevy)_