"""Buat dashboard project sebelah dengan tampilan yang sama seperti dashboard project ini.

Template diambil dari dashboard-v1/template.html lalu ditambal seperlunya (judul, nama fitur,
alasan, kartu fitur, evaluasi yang angkanya kosong, teks "Tentang"). Data dari buat_data.py.
"""
D = '/mnt/project-files/'
t = open(D + 'dashboard-v1/template.html', encoding='utf-8').read()

def ganti(old, new, n=1):
    global t
    assert t.count(old) == n, (t.count(old), old[:80])
    t = t.replace(old, new)

# --- judul dan pita atas
ganti('<title>Peta Ketidaklaziman Pengadaan</title>', '<title>Dashboard Project Sebelah</title>')
ganti('<span>Ketidaklaziman Pengadaan APBD Provinsi 2025</span>',
      '<span>Project sebelah · Anomali PBJ Provinsi 2025</span>')
ganti('<p class="lead" id="jalur-desc"></p>',
      '<p class="lead" id="jalur-desc"></p>\n  <p class="small banner">Hasil project "TRAIN ANOMALY DETECTION", ditampilkan dengan format dashboard project ini agar bisa dibandingkan. '
      'Data per paket hanya tersedia untuk 200 paket teratas nasional per jalur, dan skor IF/LOF/AE per paket tidak tersedia.</p>')
ganti('.about p {', '.banner { border: 1px solid var(--line); background: var(--accent-soft); border-radius: 10px; padding: 8px 12px; color: var(--ink-2); }\n.about p {')

# --- format angka aman untuk nilai kosong
ganti("const fmtPct = (x, d = 1) => (x * 100)", "const fmtPct = (x, d = 1) => x == null ? '–' : (x * 100)")
ganti("function rp(x) {\n", "function rp(x) {\n  if (x == null) return '–';\n")

# --- ringkasan atas
ganti("""    ['Ambang skor', j.ambang.toLocaleString('id-ID', { maximumFractionDigits: 3 }), 'Skor ensemble 0 sampai 1'],
    ['Red flag dipakai', String(Object.keys(j.rf_total).length), S.jalur === 'pelaksanaan' ? 'Termasuk 2 red flag penyedia' : 'Red flag penyedia butuh data realisasi'],""",
      """    ['Paket punya rincian', fmtInt(j.paket.length), '200 teratas nasional saja'],
    ['Red flag untuk menilai', String(j.rf_bersih.length), `dari ${Object.keys(j.rf_total).length}; ${Object.keys(j.rf_total).length - j.rf_bersih.length} bocor tidak dipakai`],""")

# --- tooltip peta: interval Wilson menggantikan pagu anomali
ganti("<br>Pagu paket tidak lazim ${rp(p.pagu_anomali)}",
      "${p.ci ? `<br>Interval 95%: ${fmtPct(p.ci[0])}–${fmtPct(p.ci[1])}` : ''}")
ganti("const mx = rows[0][1].proporsi || 1;", "const mx = rows[0][1].proporsi || 1;\n  const nas = j.nasional;")
ganti("${esc(n)}${p.n < 100 ? ' *' : ''}</span>",
      "${esc(n)}${p.n < 100 ? ' *' : ''}${p.ci && p.ci[0] > nas ? ' ▲' : (p.ci && p.ci[1] < nas ? ' ▼' : '')}</span>")
ganti('<p class="sub">Paket tidak lazim / semua paket · proporsi</p>',
      '<p class="sub">Paket tidak lazim / semua paket · proporsi. ▲/▼ = di atas/di bawah 5% nasional (interval Wilson 95%)</p>')

ganti("`Kena red flag: ${p.bukti.map((b) => lc(b.rf)).join(', ')}.`", "`Kena red flag: ${p.bukti.map((b) => b.rf).join('; ')}.`")

# --- daftar paket
ganti("$('#pk-sub').textContent = 'Diurutkan dari skor tertinggi. Titik biru = ada penjelasan SHAP dan daftar pembanding.';",
      "$('#pk-sub').textContent = 'Diurutkan dari skor tertinggi. Hanya 200 paket teratas nasional yang tersedia di data project sebelah.';")

# --- teks fitur
ganti("""const NAMA_FITUR = { pagu: 'Besar pagu', sejenis: 'Pagu dibanding paket sejenis', satker: 'Pagu dibanding paket sejenis di satker',
  nama: 'Pagu dibanding paket bernama sama', rasio: 'Realisasi dibanding pagu', selisih: 'Selisih realisasi dan pagu' };""",
      """const NAMA_FITUR = {
  z_pagu_kelompok: 'Pagu dibanding paket sejenis', z_pagu_satker: 'Pagu dibanding paket di satker',
  log_pangsa_pagu_satker: 'Porsi pagu satker yang diserap', kebulatan_pagu: 'Kebulatan pagu',
  log_pagu_kembar_satker: 'Pagu kembar di satker', pangsa_nilai_nonkompetitif_satker: 'Porsi non-kompetitif satker',
  z_rasio_real_pagu: 'Realisasi dibanding pagu', log_jangkauan_penyedia: 'Jangkauan penyedia',
  log_nilai_vs_kebiasaan_penyedia: 'Nilai dibanding kebiasaan penyedia' };
const ARTI_FITUR = {
  z_pagu_kelompok: 'Posisi pagu di antara paket berjenis dan bermetode sama se-Indonesia.',
  z_pagu_satker: 'Posisi pagu di antara semua paket satker yang sama (0 bila satker punya kurang dari 5 paket).',
  log_pangsa_pagu_satker: 'Bagian anggaran satker yang diserap paket ini.',
  kebulatan_pagu: 'Pagu yang sangat bulat sering berarti angka perkiraan, bukan hasil hitungan.',
  log_pagu_kembar_satker: 'Banyak paket di satker dengan pagu persis sama (jejak salin-tempel atau pemecahan).',
  pangsa_nilai_nonkompetitif_satker: 'Kebiasaan satker memakai metode tanpa persaingan. Angka ini sama untuk semua paket satker itu.',
  z_rasio_real_pagu: 'Posisi realisasi/pagu di antara paket sejenis dengan besar pagu serupa.',
  log_jangkauan_penyedia: 'Penyedia yang hanya melayani satu atau sedikit satker.',
  log_nilai_vs_kebiasaan_penyedia: 'Paket ini dibanding paket lain yang dikerjakan penyedia yang sama.' };""")

# alasan: poin dari kalimat project sebelah
ganti("""  const pts = (p.urut || []).map((g) => poin(p, g)).filter(Boolean).slice(0, 3);
  out.push(...(pts.length ? pts : ['Tidak ada satu angka yang sangat menonjol. Yang jarang adalah kombinasi angkanya.']));""",
      """  const pts = (p.poin || []).slice(0, 3);
  out.push(...(pts.length ? pts : ['Tidak ada satu angka yang sangat menonjol. Yang jarang adalah kombinasi angkanya.']));""")

# kartu fitur: nilai asli + arti fitur, urut SHAP
ganti("""function kartuFitur(p) {
  const fitur""", """function kartuFitur(p) {
  return (p.shap || []).map((d) => {
    const v = d[1];
    const tag = Math.abs(v) < 0.0005 ? '<span class="tag nol">tidak berpengaruh</span>'
      : `<span class="tag${v < 0 ? ' turun' : ''}">${v > 0 ? 'menaikkan' : 'menurunkan'} skor ${v > 0 ? '+' : '−'}${Math.abs(v).toLocaleString('id-ID', { minimumFractionDigits: 3, maximumFractionDigits: 3 })}</span>`;
    return `<div class="fcard"><div class="fh"><b>${esc(NAMA_FITUR[d[3]] || d[0])}</b>${tag}</div><p>${esc(d[2].charAt(0).toUpperCase() + d[2].slice(1))}.</p><p class="small">${esc(ARTI_FITUR[d[3]] || '')}</p></div>`;
  }).join('');
}
function kartuFiturLama(p) {
  const fitur""")
ganti("""      <span class="small">${p.shap ? 'Alasan diambil dari faktor SHAP yang paling menaikkan skor.' : 'Alasan diambil dari angka paket yang paling menonjol (SHAP hanya dihitung untuk 200 paket teratas nasional).'} Ini tanda untuk dicek, bukan bukti pelanggaran.</span></div>""",
      """      <span class="small">Alasan diambil dari kalimat penjelasan project sebelah (tiga faktor SHAP terbesar). Ini tanda untuk dicek, bukan bukti pelanggaran.</span></div>""")
ganti("""      <p class="small">${p.shap ? 'Urutannya sama dengan grafik SHAP di atas. Klik nama paket berwarna biru untuk membuka rinciannya; peringkat "–" berarti paket itu tidak dinilai di jalur ini.' : 'Daftar paket pembanding hanya tersedia untuk 200 paket teratas nasional (yang punya SHAP).'}</p>""",
      """      <p class="small">Urutannya sama dengan grafik SHAP di atas. Daftar paket pembanding tidak tersedia di data project sebelah.</p>""")
ganti("<h3>${p.shap ? 'Bukti tiap faktor: paket ini dibanding pembandingnya' : 'Angka paket ini dibanding pembandingnya'}</h3>",
      "<h3>Nilai tiap faktor pada paket ini</h3>")

# skor tiap model: hanya skor gabungan yang ada
ganti("const f3 = (x) => x.toLocaleString(", "const f3 = (x) => x == null ? '–' : x.toLocaleString(")
ganti("""  const models = [['Skor gabungan', p.skor, 'rata-rata tiga model'], ['Isolation Forest', p.IF, 'mudah dipisahkan dari paket lain'],
    ['LOF', p.LOF, 'jauh dari paket yang mirip'], ['Autoencoder', p.AE, 'polanya sulit ditiru ulang']];""",
      """  const models = [['Skor gabungan', p.skor, 'rata-rata tiga model, 5 seed'], ['Isolation Forest', p.IF, 'tidak tersedia'],
    ['LOF', p.LOF, 'tidak tersedia'], ['Autoencoder', p.AE, 'tidak tersedia']];""")
ganti("Skor gabungan adalah rata-rata ketiganya dan dipakai untuk mengurutkan daftar.",
      "Dashboard project sebelah hanya menyimpan skor gabungan, jadi skor tiap model tidak bisa ditampilkan.")
ganti("['Sumber transaksi', esc(p.sumber)]", "['Red flag (kode)', esc((p.kode_rf || []).join(', ') || 'tidak ada')]")

# --- evaluasi: model lain hanya punya K = 100 dan 200
ganti("const best = Math.max(...ev.filter((r) => !isBase(r)).map((r) => r['P@' + k]));",
      "const best = Math.max(...ev.filter((r) => !isBase(r) && r['P@' + k] != null).map((r) => r['P@' + k]));")
ganti("<span class=\"track\"><i style=\"width:${v * 100}%\"></i></span>",
      "<span class=\"track\"><i style=\"width:${(v || 0) * 100}%\"></i></span>")
ganti("<td class=\"num\">${r['rata_rf@' + k].toLocaleString('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>",
      "<td class=\"num\">${r['rata_rf@' + k] == null ? '–' : r['rata_rf@' + k].toLocaleString('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>")
ganti("""<p class="small" style="margin-top:8px">Red flag hanya dipakai untuk menilai, tidak dimasukkan ke model.</p>""",
      """<p class="small" style="margin-top:8px">Hanya red flag bersih yang dihitung (perencanaan P1, P4, P5, P6; pelaksanaan E3–E6). Baris Ensemble dihitung dari 200 paket teratas di dashboard project sebelah. Baris lain diambil dari laporan project sebelah, yang hanya memuat K = 100 dan 200, jadi K = 50 kosong (–). Acuan = presisi acak menurut laporan. Angka Ensemble bisa sedikit berbeda dari laporan, karena laporan merata-rata P@K tiap seed, sedangkan daftar dashboard memakai rata-rata skor 5 seed.</p>""")
ganti('<p class="sub">Bagian dari K paket teratas yang punya minimal satu red flag (Precision@K).</p>',
      '<p class="sub">Bagian dari K paket teratas yang punya minimal satu red flag bersih (Precision@K).</p>')
ganti('<p class="sub">Jumlah paket yang memenuhi tiap red flag</p>',
      '<p class="sub">Jumlah paket yang memenuhi tiap red flag. "Bocor" = bisa ditebak dari satu fitur, tidak dipakai menilai.</p>')

# --- teks atas dan "Tentang"
ganti("$('#topmeta').textContent = `${fmtInt(j.n)} paket · 38 provinsi · TA 2025`;",
      "$('#topmeta').textContent = `${fmtInt(j.n)} paket · 38 provinsi · TA 2025 · project sebelah`;")
i0 = t.index('    <p><b>Sumber data:</b>')
i1 = t.index('    </div>\n  </details>\n</main>')
t = t[:i0] + """    <p><b>Sumber:</b> dashboard dan laporan project "TRAIN ANOMALY DETECTION" (RUP dan realisasi APBD provinsi 2025, INAPROC). Lingkup project itu: paket penyedia, pagu minimal Rp1.000 (bukan Rp1 juta seperti project ini). Jalur pelaksanaan: paket dengan realisasi selesai (Serah Terima), dibersihkan dari rasio realisasi/pagu yang tidak masuk akal.</p>
    <p><b>Model project sebelah:</b> Isolation Forest + LOF + Autoencoder, skor tiap model diubah ke persentil lalu dirata-rata, diulang 5 seed. Paket "tidak lazim" = 5% skor tertinggi nasional. Fitur perencanaan (6): posisi pagu di antara paket sejenis, posisi pagu di satker, porsi pagu satker yang diserap, kebulatan pagu, pagu kembar di satker, porsi non-kompetitif satker. Pelaksanaan menambah 3: posisi realisasi/pagu, jangkauan penyedia, dan nilai dibanding kebiasaan penyedia.</p>
    <p><b>Red flag:</b> 12 (P1–P6 perencanaan, E1–E6 pelaksanaan). Empat di antaranya (P2, P3, E1, E2) bocor karena dihitung dari angka yang sama dengan fitur, jadi hanya red flag bersih yang dipakai untuk Precision@K.</p>
    <p><b>Yang berbeda dari dashboard project ini:</b> hanya 200 paket teratas per jalur yang punya rincian, skor IF/LOF/AE per paket dan daftar paket pembanding tidak tersedia, alasan poin diambil dari kalimat project sebelah, dan peta memakai interval Wilson 95% (▲/▼).</p>
""" + t[i1:]

import json
data = open(D + 'dashboard-sebelah/dashboard-data-sebelah.json', encoding='utf-8').read()
geo = open(D + 'dashboard-v1/provinsi38.geojson', encoding='utf-8').read()
json.loads(data), json.loads(geo)
safe = lambda s: s.replace('</', '<\\/')  # noqa: E731
out = t.replace('__DATA__', safe(data)).replace('__GEO__', safe(geo))
open(D + 'dashboard-sebelah/template-sebelah.html', 'w', encoding='utf-8').write(t)
open(D + 'dashboard-sebelah/dashboard-sebelah.html', 'w', encoding='utf-8').write(out)
print(len(out.encode()) // 1024, 'KB')
