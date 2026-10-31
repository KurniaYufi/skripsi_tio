import pandas as pd
pd.set_option('display.width', 250)
d = pd.read_csv('/mnt/project-files/eksperimen-lanjutan/e_eval.csv')
d['kol'] = d.jalur.str.slice(0, 4) + ' ' + d.tahun.astype(str) + ' ' + d.provinsi
for v in ['lipat 5% (tanpa paket RF2)', 'lipat 5%', 'P@200 (tanpa paket RF2)', 'P@200']:
    print('##', v)
    print(d.pivot_table(index=['varian', 'gabungan'], columns='kol', values=v).round(2).to_string())
