import zipfile, os
src = 'HeroesOldenEra_Data/StreamingAssets/Core.zip'
dst = 'catalog/raw'
os.makedirs(dst, exist_ok=True)
with zipfile.ZipFile(src) as z:
    for info in z.infolist():
        name = info.filename
        if not info.flag_bits & 0x800:
            try: name = name.encode('cp437').decode('utf-8')
            except Exception: pass
        out = os.path.join(dst, name)
        if name.endswith('/'):
            os.makedirs(out, exist_ok=True); continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with z.open(info) as s, open(out, 'wb') as d:
            d.write(s.read())
            