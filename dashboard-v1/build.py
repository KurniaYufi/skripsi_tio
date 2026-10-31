"""Gabungkan template, data model, dan GeoJSON menjadi satu file dashboard.html."""
import json
import sys

D = '/mnt/project-files/'
t = open(D + 'dashboard-v1/template.html', encoding='utf-8').read()
model = sys.argv[1] if len(sys.argv) > 1 else 'model-v2'
data = open(D + model + '/dashboard-data.json', encoding='utf-8').read()
geo = open(D + 'dashboard-v1/provinsi38.geojson', encoding='utf-8').read()
safe = lambda s: s.replace('</', '<\\/')  # noqa: E731  (cegah penutupan tag script di dalam JSON)
json.loads(data), json.loads(geo)
out = t.replace('__DATA__', safe(data)).replace('__GEO__', safe(geo))
open(D + 'dashboard-v1/dashboard.html', 'w', encoding='utf-8').write(out)
# Versi mandiri untuk dibuka langsung di peramban atau di-host sendiri (mis. GitHub Pages)
head = ('<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
i = out.index('</style>') + len('</style>')
mandiri = head + out[:i] + '\n</head>\n<body>\n' + out[i:] + '\n</body>\n</html>\n'
open(D + 'dashboard-v1/dashboard-mandiri.html', 'w', encoding='utf-8').write(mandiri)
print(len(out.encode()) // 1024, 'KB')
