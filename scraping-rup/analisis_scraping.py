"""Analisis hasil scraping uji coba: apakah paket teratas model lebih sering punya informasi yang tidak terbuka?

    python analisis_scraping.py

Membaca hasil/detail_rup.csv + sampel_scraping.csv, lalu menulis:
    hasil/tanda_per_paket.csv    tanda turunan per paket (uraian/spesifikasi tidak informatif, volume, jadwal)
    hasil/ringkasan.md           perbandingan kelompok teratas vs acak
"""
import math, re
from pathlib import Path

import pandas as pd

DIR = Path(__file__).resolve().parent
OUT = DIR / 'hasil'
BULAN = {b: i for i, b in enumerate(['januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus',
                                     'september', 'oktober', 'november', 'desember'], 1)}

# Teks yang hanya merujuk dokumen lain (KAK/TOR/lampiran), tanpa menjelaskan pekerjaannya
RUJUK = re.compile(r'\b(uraian|spesifikasi)?\s*(pekerjaan)?\s*(ada\s+)?(pada|sesuai|dalam|lihat|di|terlampir( pada| dalam)?|mengacu( pada)?|berdasarkan)'
                   r'\s+(kak|tor|kerangka acuan( kerja)?|dokumen|lampiran|rab|hps|spesifikasi teknis)\b', re.I)


def norm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', str(s).lower()).split()


def tidak_informatif(teks, nama):
    """'kosong' / 'rujuk_kak' / 'sama_nama' / '' (informatif)."""
    if not isinstance(teks, str) or len(teks.strip()) < 5 or teks.strip() in {'-', '.', '0'}:
        return 'kosong'
    sisa = RUJUK.sub(' ', teks)
    if RUJUK.search(teks) and len(' '.join(norm(sisa))) < 25:
        return 'rujuk_kak'
    if norm(teks) == norm(nama):
        return 'sama_nama'
    return ''


def bulan(s):
    m = re.match(r'\s*([A-Za-z]+)\s+(\d{4})', str(s))
    if not m or m.group(1).lower() not in BULAN:
        return None
    return int(m.group(2)) * 12 + BULAN[m.group(1).lower()] - 1


def volume_satuan(v):
    """Jumlah satuan kalau volume berupa angka selain '1 paket' (mis. '88x13' -> 1144, '12 Bulan' -> 12)."""
    if not isinstance(v, str):
        return None
    v2 = re.sub(r'(?<=\d)\.(?=\d{3}\b)', '', v)  # 1.144 -> 1144
    angka = [float(x.replace(',', '.')) for x in re.findall(r'\d+(?:,\d+)?', v2)]
    if not angka:
        return None
    n = math.prod(angka)
    return None if n == 1 else n


def uji_dua_proporsi(x1, n1, x2, n2):
    if min(n1, n2) == 0:
        return float('nan')
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return float('nan') if se == 0 else math.erfc(abs(x1 / n1 - x2 / n2) / se / math.sqrt(2))


def main():
    d = pd.read_csv(OUT / 'detail_rup.csv', dtype=str)
    s = pd.read_csv(DIR / 'sampel_scraping.csv', dtype={'kode_rup': str})
    d = s[['kode_rup', 'kelompok', 'peringkat', 'nama_paket']].merge(d, on='kode_rup', how='inner')
    nama = d['Nama Paket'].fillna(d.nama_paket)
    t = pd.DataFrame({'kode_rup': d.kode_rup, 'kelompok': d.kelompok, 'peringkat': d.peringkat})
    t['uraian'] = [tidak_informatif(a, b) for a, b in zip(d['Uraian Pekerjaan'], nama)]
    t['spesifikasi'] = [tidak_informatif(a, b) for a, b in zip(d['Spesifikasi Pekerjaan'], nama)]
    t['uraian_tidak_informatif'] = t.uraian != ''
    t['spesifikasi_tidak_informatif'] = t.spesifikasi != ''
    t['keduanya_tidak_informatif'] = t.uraian_tidak_informatif & t.spesifikasi_tidak_informatif
    t['keduanya_rujuk_kak'] = (t.uraian == 'rujuk_kak') & (t.spesifikasi == 'rujuk_kak')
    t['volume_satuan'] = d['Volume Pekerjaan'].map(volume_satuan)
    t['volume_berangka'] = t.volume_satuan.notna()
    pm, pa = d['Jadwal Pemilihan Penyedia Mulai'].map(bulan), d['Jadwal Pemilihan Penyedia Akhir'].map(bulan)
    km, ka = d['Jadwal Pelaksanaan Kontrak Mulai'].map(bulan), d['Jadwal Pelaksanaan Kontrak Akhir'].map(bulan)
    t['pemilihan_akhir_nov_des'] = pa.map(lambda x: x is not None and x % 12 >= 10)
    t['pemilihan_mulai_sebelum_2025'] = pm.map(lambda x: x is not None and x < 2025 * 12)
    t['durasi_kontrak_bulan'] = [b - a + 1 if a is not None and b is not None else None for a, b in zip(km, ka)]
    t['kontrak_1_bulan'] = t.durasi_kontrak_bulan == 1
    t['jadwal_tidak_konsisten'] = [a is not None and b is not None and b < a for a, b in zip(pm, km)]
    t['pra_dipa'] = d['Pra DIPA / DPA'].eq('Ya')
    t.to_csv(OUT / 'tanda_per_paket.csv', index=False)

    tanda = ['uraian_tidak_informatif', 'spesifikasi_tidak_informatif', 'keduanya_tidak_informatif', 'keduanya_rujuk_kak',
             'volume_berangka', 'pemilihan_akhir_nov_des', 'pemilihan_mulai_sebelum_2025', 'kontrak_1_bulan',
             'jadwal_tidak_konsisten', 'pra_dipa']
    a, b = t[t.kelompok == 'teratas'], t[t.kelompok == 'acak']
    baris = ['| Tanda | Teratas | Acak | Selisih (poin) | p |', '|---|---|---|---|---|']
    for c in tanda:
        x1, x2 = int(a[c].sum()), int(b[c].sum())
        p1, p2 = x1 / max(len(a), 1), x2 / max(len(b), 1)
        baris.append(f'| {c} | {p1:.1%} ({x1}/{len(a)}) | {p2:.1%} ({x2}/{len(b)}) | {100 * (p1 - p2):+.1f} | {uji_dua_proporsi(x1, len(a), x2, len(b)):.3f} |')
    contoh = d.loc[t.keduanya_tidak_informatif.values, ['kode_rup', 'kelompok', 'Uraian Pekerjaan', 'Spesifikasi Pekerjaan']].head(15)
    md = ['# Ringkasan uji coba scraping', '',
          f'Paket berhasil: {len(t)} (teratas {len(a)}, acak {len(b)}).', '',
          'p = uji dua proporsi; p < 0,05 berarti beda teratas vs acak kemungkinan bukan kebetulan.', '', *baris, '',
          '## Contoh paket dengan uraian dan spesifikasi tidak informatif', '',
          *(['| ' + ' | '.join(str(x).replace('|', '/') for x in r) + ' |' for r in [contoh.columns, ['---'] * 4, *contoh.values.tolist()]] if len(contoh) else ['(tidak ada)'])]
    (OUT / 'ringkasan.md').write_text('\n'.join(md), encoding='utf-8')
    print('\n'.join(md[:8 + len(baris)]))


if __name__ == '__main__':
    main()
