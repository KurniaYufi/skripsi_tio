# Draf Penambahan LLM pada Bab 1, Bab 2, dan Bab 3

Draf 2026-10-28, disusun setelah Tio memutuskan memakai LLM untuk menyusun kalimat penjelasan SHAP. Belum dimasukkan ke Google Doc. Rencananya masuk ke tab baru per bab, digabung dengan keputusan red flag dan fitur.

Teks **tebal** di bawah adalah teks baru atau teks yang diubah. Teks lain sama dengan versi sekarang.

---

## A. Referensi baru (semua gratis)

| Referensi | Dipakai untuk | Akses gratis | Status |
|---|---|---|---|
| Padín-Torrente, H., Carneiro-Diaz, V., & Ortega-Fernandez, I. (2026). Toward human-centered explainability: Natural language explanations for anomaly detection. *Information Systems Frontiers*. https://doi.org/10.1007/s10796-026-10717-3 | Penelitian terdahulu (2.1.4), Bab 1, Bab 3 | Lisensi CC BY 4.0. PDF: https://ruc.udc.es/bitstreams/080360a5-5b4c-418a-a931-bb2147cf78b4/download | Sudah dibaca isinya. **Perlu diunggah Tio ke Library** |
| Martens, D., Hinns, J., Dams, C., Vergouwen, M., & Evgeniou, T. (2024). *Tell me a story! Narrative-driven XAI with large language models* (arXiv:2309.17057). arXiv. https://arxiv.org/abs/2309.17057 | Bab 1 dan 2.2.11: SHAP terlalu teknis bagi pengguna awam | arXiv, gratis | Abstrak dan bagian metode sudah dicek. Preprint, belum ada versi jurnal yang tercatat di arXiv |
| Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., & Liu, T. (2025). A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. *ACM Transactions on Information Systems, 43*(2). https://doi.org/10.1145/3703155 | 2.2.11: halusinasi | Versi arXiv gratis: https://arxiv.org/abs/2311.05232 | DOI sudah dicek. **Nomor artikel perlu dicek dari PDF** |
| Naveed, H., Khan, A. U., Qiu, S., Saqib, M., Anwar, S., Usman, M., Akhtar, N., Barnes, N., & Mian, A. (2025). A comprehensive overview of large language models. *ACM Transactions on Intelligent Systems and Technology*. | 2.2.11: pengertian LLM | Versi arXiv gratis: https://arxiv.org/abs/2307.06435 | Baru abstraknya yang dicek. **Volume, nomor, dan DOI perlu dicek dari PDF** |

Sumber yang ditemukan tapi tidak dipakai: Zytek et al. (2024), Explingo (arXiv:2412.05145). Isinya mirip Martens et al. (2024), jadi cukup satu.

---

## B. Bab 1

### B.1 Latar Belakang, paragraf XAI (paragraf ke-4)

Selain itu, sebagian besar model machine learning bekerja seperti black box, yaitu menghasilkan skor anomali tanpa menjelaskan alasan di balik skor tersebut (Roshan & Zafar, 2021). Akibatnya, alasan mengapa suatu data dianggap anomali menjadi sulit untuk dipahami, khususnya pada deteksi anomali yang tidak menggunakan label (Roshan & Zafar, 2021). Salah satu metode penjelasan yang dapat digunakan adalah SHapley Additive exPlanations (SHAP), yang mampu menunjukkan fitur yang paling memengaruhi skor anomali, termasuk pada model Autoencoder (Roshan & Zafar, 2021). **Namun, hasil SHAP berupa angka kontribusi setiap fitur sering kali terlalu teknis untuk dipahami dan ditindaklanjuti oleh pengguna awam (Martens et al., 2024). Untuk mengatasi hal tersebut, Large Language Model (LLM) dapat digunakan untuk mengubah hasil SHAP menjadi kalimat penjelasan, termasuk pada deteksi anomali berbasis Autoencoder (Padín-Torrente et al., 2026).** Selain dapat dijelaskan, hasil deteksi juga perlu mudah diakses oleh pengguna. Menurut penelitian Schneider dos Santos et al. (2025), dari 93 studi yang ditelaah, hanya dua yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas.

### B.2 Latar Belakang, paragraf usulan (paragraf terakhir)

Kalimat "SHAP digunakan untuk menjelaskan fitur yang paling memengaruhi skor anomali yang dihasilkan." diganti menjadi:

**SHAP digunakan untuk menjelaskan fitur yang paling memengaruhi skor anomali yang dihasilkan, kemudian hasilnya disusun menjadi kalimat penjelasan menggunakan LLM.**

### B.3 Rumusan Masalah nomor 2

Bagaimana menerapkan SHAP untuk menjelaskan kontribusi fitur terhadap skor anomali pada paket pengadaan yang diprioritaskan**, serta menyusun hasilnya menjadi kalimat penjelasan menggunakan LLM**?

### B.4 Tujuan nomor 2

Menerapkan SHAP untuk menjelaskan kontribusi fitur terhadap skor anomali pada paket pengadaan yang diprioritaskan**, serta menyusun hasilnya menjadi kalimat penjelasan menggunakan LLM**.

### B.5 Batasan Masalah nomor 6

Penjelasan hasil menggunakan SHAP dan hanya diterapkan pada paket dengan skor anomali tertinggi. **LLM hanya digunakan untuk menyusun kalimat penjelasan dari hasil SHAP, tidak digunakan untuk menghitung skor anomali, dan kesesuaian kalimat yang dihasilkan diperiksa terhadap hasil SHAP.**

### B.6 Manfaat ilmiah nomor 2

Menunjukkan penggunaan explainable AI berbasis SHAP **yang dilengkapi kalimat penjelasan dari LLM** untuk menjelaskan skor anomali pada data pengadaan publik di Indonesia.

---

## C. Bab 2

### C.1 Penelitian terdahulu: tambahan di akhir 2.1.4 Penerapan SHAP pada Deteksi Anomali

Paragraf baru, diletakkan sebelum paragraf penutup 2.1.4 ("Kedua penelitian tersebut mendukung ...", yang diubah menjadi "Ketiga penelitian tersebut ...").

**Hasil SHAP berupa angka kontribusi fitur masih perlu diterjemahkan agar mudah dipahami oleh pemeriksa. Penelitian yang dilakukan Padín-Torrente et al. (2026) menggunakan LLM untuk mengubah hasil deteksi anomali dan SHAP menjadi kalimat penjelasan bagi analis keamanan jaringan. Data yang digunakan adalah dataset CSE-CIC-IDS2018, dengan Autoencoder sebagai model deteksi anomali yang mencapai ROC-AUC 91,14% dan F1 80,24%. Untuk setiap data yang ditandai, dipilih tiga fitur dengan galat rekonstruksi terbesar, lalu Kernel SHAP digunakan untuk menghitung kontribusi fitur terhadap galat tersebut. Hasilnya diberikan kepada lima LLM yang dijalankan secara lokal, dengan ukuran 4 hingga 32 miliar parameter, menggunakan tiga cara pemberian instruksi, yaitu tanpa konteks, dengan konteks dan format yang ditetapkan, serta dengan contoh penjelasan dari pakar melalui retrieval-augmented generation (RAG). Kalimat yang dihasilkan dinilai menggunakan rubrik yang mencakup ketepatan isi terhadap hasil SHAP, kejelasan, relevansi, keringkasan, dan pemahaman terhadap ancaman. Hasilnya menunjukkan bahwa pemberian konteks dan pengetahuan manusia lebih berpengaruh terhadap kualitas kalimat daripada ukuran model, dengan nilai ketepatan isi tertinggi 9,06 dari 10 pada cara RAG. Namun, penelitian ini menegaskan bahwa kalimat penjelasan bergantung pada hasil Autoencoder, sehingga tidak dapat memperbaiki data yang salah ditandai, dan belum diuji langsung kepada pengguna.**

Paragraf penutup 2.1.4 (perubahan):

**Ketiga** penelitian tersebut mendukung penggunaan SHAP untuk menjelaskan alasan setiap paket diprioritaskan pada tugas akhir ini, termasuk pada komponen Autoencoder. Cara Herreros-Martínez et al. (2025) ... [tetap]. Catatan tentang waktu komputasi SHAP ... [tetap]. **Cara Padín-Torrente et al. (2026) yang hanya memberikan tiga fitur teratas kepada LLM dan menilai ketepatan kalimat terhadap hasil SHAP juga menjadi acuan penyusunan kalimat penjelasan pada tugas akhir ini.** Perbedaannya, **ketiga** penelitian tersebut tidak menggunakan data pengadaan pemerintah, sedangkan tugas akhir ini menjelaskan skor ensemble pada paket pengadaan APBD pemerintah provinsi.

### C.2 Tabel 2.1: baris baru (setelah Roshan & Zafar)

| Judul Penelitian | Dataset | Metode | Hasil |
|---|---|---|---|
| Toward Human-Centered Explainability: Natural Language Explanations for Anomaly Detection (Padín-Torrente et al., 2026) | Dataset CSE-CIC-IDS2018 (lalu lintas jaringan) | Autoencoder, Kernel SHAP, lima LLM lokal (4–32 miliar parameter), RAG | Konteks dan pengetahuan pakar lebih berpengaruh daripada ukuran model; ketepatan isi tertinggi 9,06 dari 10. Bukan data pengadaan dan belum diuji kepada pengguna. |

### C.3 Paragraf kesenjangan (setelah Tabel 2.1)

Tambahan pada kalimat terakhir:

... yang menilai setiap paket sejak tahap perencanaan, dilengkapi penjelasan SHAP **yang disusun menjadi kalimat dengan LLM**, dan disajikan dalam dashboard untuk membantu pengawas menentukan paket yang perlu ditelusuri lebih lanjut.

### C.4 Dasar Teori: subbab baru 2.2.11 Large Language Model (LLM)

Diletakkan setelah 2.2.10 SHAP dan Interpretasi Model. Metrik Evaluasi bergeser menjadi 2.2.12, Dashboard dan Peta Choropleth menjadi 2.2.13. Nomor persamaan dan gambar tidak berubah karena subbab ini tidak memuat persamaan atau gambar.

**2.2.11 Large Language Model (LLM)**

**Large Language Model (LLM) adalah model bahasa berukuran besar yang dilatih menggunakan data teks dalam jumlah sangat besar sehingga mampu memahami dan menghasilkan teks dalam bahasa alami (Naveed et al., 2025). LLM dapat menjalankan berbagai tugas bahasa, seperti meringkas dan menyusun kalimat, berdasarkan instruksi yang diberikan dalam bentuk teks yang disebut prompt (Naveed et al., 2025).**

**Dalam explainable AI, LLM dapat digunakan untuk mengubah hasil SHAP menjadi kalimat penjelasan. Hal ini diperlukan karena hasil SHAP sering kali terlalu teknis untuk dipahami pengguna awam (Martens et al., 2024). Martens et al. (2024) memberikan nilai fitur dan nilai SHAP suatu data kepada LLM, lalu meminta LLM hanya menjelaskan fitur dengan kontribusi terbesar dalam beberapa kalimat. Pengguna yang membaca kalimat tersebut lebih sering menjawab pertanyaan pemahaman dengan benar dibandingkan pengguna yang hanya melihat nilai SHAP (Martens et al., 2024).**

**Meskipun demikian, LLM dapat mengalami halusinasi, yaitu menghasilkan kalimat yang terdengar meyakinkan tetapi tidak sesuai fakta (Huang et al., 2025). Kalimat penjelasan dari LLM juga dapat terlalu umum atau tidak sesuai dengan perilaku model yang dijelaskan (Padín-Torrente et al., 2026). Oleh karena itu, masukan kepada LLM perlu dibatasi pada hasil SHAP yang sudah dihitung, instruksi perlu memuat konteks dan format yang jelas, dan kalimat yang dihasilkan perlu diperiksa kesesuaiannya dengan hasil SHAP (Padín-Torrente et al., 2026).**

**Dalam tugas akhir ini, LLM digunakan setelah SHAP untuk menyusun kalimat penjelasan bagi paket berperingkat atas. LLM tidak digunakan untuk menghitung skor anomali, sehingga kalimat yang dihasilkan hanya menerangkan hasil SHAP.**

### C.5 Penutup 2.2.10 SHAP (tambahan satu kalimat)

Dalam tugas akhir ini, SHAP digunakan setelah skor gabungan diperoleh untuk menjelaskan fitur yang paling memengaruhi skor paket berperingkat atas. Penjelasan ini membantu pengguna memahami alasan suatu paket diprioritaskan. **Hasil SHAP tersebut kemudian disusun menjadi kalimat penjelasan menggunakan LLM yang diuraikan pada Subbab 2.2.11.**

### C.6 Penutup 2.2.13 Dashboard (perubahan kecil)

Dalam tugas akhir ini, dashboard digunakan untuk menyajikan sebaran paket anomali antarprovinsi, peringkat paket, dan penjelasan SHAP **beserta kalimat penjelasannya** untuk setiap paket. [kalimat berikutnya tetap]

---

## D. Bab 3

### D.1 3.2.2 Studi Literatur

- Fokus penelitian terdahulu: ... dan penerapan SHAP pada deteksi anomali **serta penyusunan kalimat penjelasan dengan LLM**.
- Dasar teori: ... ensemble deteksi anomali, SHAP, **Large Language Model (LLM)**, metrik evaluasi, serta dashboard dan peta choropleth.

### D.2 3.2.5 Evaluasi dan Interpretasi Model (paragraf pembuka)

Kalimat "Setelah itu, SHAP digunakan untuk menjelaskan kontribusi fitur terhadap skor paket berperingkat atas." diganti:

**Setelah itu, SHAP digunakan untuk menjelaskan kontribusi fitur terhadap skor paket berperingkat atas, lalu hasilnya disusun menjadi kalimat penjelasan menggunakan LLM dan diperiksa kesesuaiannya.**

Kalimat setelah Gambar 3.7 juga ditambah: "... lalu paket berperingkat atas ditelaah berdasarkan jumlah red flag, dijelaskan menggunakan SHAP, **dan dibuatkan kalimat penjelasan menggunakan LLM**."

Luaran di akhir 3.2.5.5 dipindah ke subbab baru terakhir (3.2.5.7).

### D.3 Subbab baru 3.2.5.6 Penyusunan Kalimat Penjelasan dengan LLM

**Hasil SHAP setiap paket berperingkat atas disusun menjadi kalimat penjelasan menggunakan LLM agar lebih mudah dipahami oleh pengawas (Martens et al., 2024). Masukan yang diberikan kepada LLM dibatasi pada tiga fitur dengan kontribusi SHAP terbesar, mengikuti Padín-Torrente et al. (2026). Untuk setiap fitur, masukan memuat nama fitur dalam bahasa sehari-hari, nilai fitur pada paket tersebut, nilai pembanding seperti median paket sejenis, serta arah kontribusinya terhadap skor. Instruksi kepada LLM dibuat tetap untuk semua paket dan memuat konteks pengadaan serta format jawaban, karena pemberian konteks lebih berpengaruh terhadap kualitas kalimat daripada ukuran model (Padín-Torrente et al., 2026). Instruksi tersebut meminta LLM menulis paling banyak tiga kalimat, hanya menggunakan angka yang diberikan, dan hanya menyebut ketidaklaziman tanpa menyimpulkan adanya pelanggaran. LLM yang digunakan adalah model open-source yang dijalankan secara lokal, seperti pada Padín-Torrente et al. (2026), sehingga hasilnya dapat diulang. Kalimat dibuat satu kali untuk setiap paket berperingkat atas lalu disimpan, sehingga dashboard tidak perlu memanggil LLM setiap kali paket dibuka.**

### D.4 Subbab baru 3.2.5.7 Pemeriksaan Kalimat Penjelasan

**Karena LLM dapat menghasilkan kalimat yang terdengar meyakinkan tetapi tidak sesuai fakta (Huang et al., 2025), setiap kalimat diperiksa sebelum disimpan. Pemeriksaan dilakukan secara otomatis dengan tiga aturan. Pertama, fitur yang disebut dalam kalimat harus sama dengan tiga fitur yang diberikan. Kedua, setiap angka dalam kalimat harus sama dengan angka pada masukan. Ketiga, kalimat tidak boleh memuat kata yang menyimpulkan pelanggaran. Kalimat yang tidak lolos pemeriksaan dibuat ulang satu kali. Jika masih tidak lolos, kalimat diganti dengan kalimat templat yang disusun dari hasil SHAP, misalnya "Pagu paket ini 8 kali lebih besar dari median paket sejenis." Jumlah kalimat yang lolos pemeriksaan dicatat untuk melihat ketepatan LLM. Grafik kontribusi fitur dari SHAP tetap ditampilkan bersama kalimat agar pengguna dapat mencocokkan penjelasannya. Luaran tahap ini adalah hasil evaluasi, kontribusi fitur, dan kalimat penjelasan untuk setiap paket berperingkat atas.**

### D.5 3.2.6.2 Perancangan Dashboard (komponen keempat)

Keempat, rincian paket yang memuat data paket, skor anomali, grafik kontribusi fitur dari SHAP, **dan kalimat penjelasan dari LLM**.

### D.6 3.2.7 Analisis Hasil dan Pembahasan

Analisis mencakup perbandingan kinerja ensemble dengan model individual, fitur yang paling sering memengaruhi skor paket berperingkat atas, **jumlah kalimat penjelasan yang lolos pemeriksaan,** serta provinsi dengan proporsi paket anomali yang tinggi pada setiap jalur.

### D.7 Gambar yang diperbarui

Sudah dibuat: /mnt/project-files/bab3/gambar/gambar-3-2-metodologi-bagian-2-v4.png dan /mnt/project-files/bab3/gambar/gambar-3-7-diagram-alir-evaluasi-model-v2.png (script gambar-3-metodologi-v4.py dan gambar-3-diagram-alir-v2.py).


- **Gambar 3.2** (diagram metodologi bagian 2): setelah "Interpretasi dengan SHAP", tambah "Penyusunan Kalimat Penjelasan dengan LLM" dan "Pemeriksaan Kalimat Penjelasan".
- **Gambar 3.7** (diagram alir evaluasi): setelah "Perhitungan SHAP pada paket peringkat teratas", tambah proses LLM, keputusan "Kalimat lolos pemeriksaan?" (Tidak: buat ulang atau ganti templat), lalu luaran "Hasil evaluasi, kontribusi fitur, dan kalimat penjelasan".

---

## E. Pilihan default yang aku ambil (bisa diubah)

| Hal | Default | Alasan |
|---|---|---|
| Jenis LLM | Open-source, dijalankan lokal (nama model ditentukan di Bab 4) | Mengikuti Padín-Torrente et al. (2026); hasil bisa diulang dan tanpa biaya API |
| Jumlah fitur yang dijelaskan | 3 fitur SHAP terbesar | Mengikuti Padín-Torrente et al. (2026) |
| Cara menilai kalimat | Pemeriksaan otomatis (nama fitur, angka, kata terlarang) | Sederhana dan bisa dihitung. Tidak memakai LLM sebagai penilai dan tidak ada uji ke pengguna, supaya ruang lingkup tidak melebar |
| Templat tanpa LLM | Cadangan bila kalimat LLM gagal pemeriksaan, bukan pembanding | Lebih ringan daripada membandingkan dua cara |
