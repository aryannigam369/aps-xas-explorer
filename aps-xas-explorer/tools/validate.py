"""Validate data integrity and the static distribution. Standard library only."""
from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'src/data.json').read_text());q=d['queries']
cat=q['catalog']['rows'];rows=q['spectra']['rows'];files=q['files']['rows']
assert len(cat)==33 and len(rows)==15939 and len(files)==39
assert len({s['id'] for s in cat})==33
for s in cat:
    pts=[r for r in rows if r['scanId']==s['id']]
    assert len(pts)==483, s['file']
    assert all(a['energyEv']<b['energyEv'] for a,b in zip(pts,pts[1:]))
    assert all(x['i0']>0 and math.isclose(x['fluoA'],x['flatot']/x['i0']) and math.isclose(x['fluoB'],x['flbtot']/x['i0']) for x in pts)
    assert all(math.isclose(x['relativeEv'],x['energyEv']-s['edgeEv'],abs_tol=1e-6) for x in pts)
for f in files:
    assert hashlib.sha256((ROOT/'public/raw'/f['file']).read_bytes()).hexdigest()==f['sha256'], f['file']
    if (ROOT/'dist/raw').exists():
        assert hashlib.sha256((ROOT/'dist/raw'/f['file']).read_bytes()).hexdigest()==f['sha256'],f['file']
assert len(q['inventory']['rows'])==52
assert sum(r['points'] for r in q['inventory']['rows'])==17872
assert sum('conflict' in r['flags'] for r in cat)==3
assert sum(r['sample']=='T1' and r['element']=='Cu' for r in cat)==3
assert sum(r['points'] for r in q['inventory']['rows'] if r['scope']!='Main spectroscopy')==1933
print('PASS: 33 spectra, 15,939 points, 52 blocks, 17,872 acquisition rows.')
print('PASS: monotonic energies, finite positive I0, derived ratios, relative energies, source SHA-256 checks, and block separation.')
print('Browser rendering and interactive behavior require a separate visual check.')
